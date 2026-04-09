import socket
import ssl
import threading

HOST = '127.0.0.1'
PORT = 5000

# Seats S1–S20
seats = {f"S{i}": None for i in range(1, 21)}

lock = threading.Lock()

# ================= VALIDATION =================
def is_valid_seat(seat):
    if not seat.startswith("S"):
        return False
    if not seat[1:].isdigit():
        return False
    num = int(seat[1:])
    return 1 <= num <= 20

# ================= CLIENT HANDLER =================
def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")
    conn.settimeout(60)

    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            print(f"[REQUEST] {addr} → {data}")
            response = process_request(data)
            conn.send(response.encode())

    except Exception as e:
        print(f"[ERROR] {addr}: {e}")

    finally:
        print(f"[DISCONNECTED] {addr}")
        conn.close()

# ================= REQUEST PROCESSOR =================
def process_request(request):
    parts = request.strip().split()

    if len(parts) == 0:
        return "400 INVALID_FORMAT"

    command = parts[0]

    # -------- BOOK --------
    if command == "BOOK":
        if len(parts) != 3:
            return "400 INVALID_FORMAT"

        seat, user = parts[1], parts[2]

        if not is_valid_seat(seat):
            return "400 INVALID_SEAT"

        with lock:
            if seats[seat] is None:
                seats[seat] = user
                save_to_file()
                return "200 SUCCESS"
            else:
                return "409 ALREADY_BOOKED"

    # -------- STATUS --------
    elif command == "STATUS":
        if len(parts) != 2:
            return "400 INVALID_FORMAT"

        seat = parts[1]

        if not is_valid_seat(seat):
            return "400 INVALID_SEAT"

        if seats[seat] is None:
            return "200 AVAILABLE"
        else:
            return f"200 BOOKED_BY {seats[seat]}"

    # -------- CANCEL --------
    elif command == "CANCEL":
        if len(parts) != 3:
            return "400 INVALID_FORMAT"

        seat, user = parts[1], parts[2]

        if not is_valid_seat(seat):
            return "400 INVALID_SEAT"

        with lock:
            if seats[seat] == user:
                seats[seat] = None
                save_to_file()
                return "200 CANCELLED"
            else:
                return "403 NOT_OWNER"

    # -------- VIEW --------
    elif command == "VIEW":
        result = []
        for seat, user in seats.items():
            status = user if user else "EMPTY"
            result.append(f"{seat}:{status}")
        return "200 " + " ".join(result)

    else:
        return "400 INVALID_COMMAND"

# ================= FILE HANDLING =================
def save_to_file():
    with open("bookings.txt", "w") as f:
        for seat, user in seats.items():
            if user:
                f.write(f"{seat} {user}\n")

def load_from_file():
    try:
        with open("bookings.txt", "r") as f:
            for line in f:
                seat, user = line.strip().split()
                if seat in seats:
                    seats[seat] = user
    except FileNotFoundError:
        pass

# ================= SERVER START =================
def start_server():
    load_from_file()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)

    print("🎬 Secure Movie Seat Server running on port 5000...")

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    while True:
        client_socket, addr = sock.accept()
        secure_conn = context.wrap_socket(client_socket, server_side=True)

        thread = threading.Thread(target=handle_client, args=(secure_conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()