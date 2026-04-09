import socket
import ssl

HOST = '127.0.0.1'
PORT = 5000

def start_client():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_sock = context.wrap_socket(sock, server_hostname=HOST)

    secure_sock.connect((HOST, PORT))
    print("✅ Connected to Secure Movie Server")

    while True:
        print("\n===== MENU =====")
        print("1. Book Seat")
        print("2. Check Seat Status")
        print("3. Cancel Booking")
        print("4. View All Seats")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            seat = input("Seat (S1–S20): ")
            user = input("Your name: ")
            message = f"BOOK {seat} {user}"

        elif choice == "2":
            seat = input("Seat: ")
            message = f"STATUS {seat}"

        elif choice == "3":
            seat = input("Seat: ")
            user = input("Your name: ")
            message = f"CANCEL {seat} {user}"

        elif choice == "4":
            message = "VIEW"

        elif choice == "5":
            print("👋 Exiting...")
            break

        else:
            print("❌ Invalid choice")
            continue

        secure_sock.send(message.encode())
        response = secure_sock.recv(1024).decode()
        print("📩 Server:", response)

    secure_sock.close()

if __name__ == "__main__":
    start_client()