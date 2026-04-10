Secure Movie Seat Booking System
Problem Statement
This project implements a secure multi-client movie seat booking system using socket programming with SSL/TLS encryption.
---
Features
* Multi-client support using threading
* Secure communication using SSL/TLS
* Seat booking, cancellation, and status check
* File-based persistence
* Concurrency control using locks
---
Architecture
Client → SSL Socket → Server → Seat Manager → File Storage

---
Protocol Design
| Command        | Description    |
| -------------- | -------------- |
| BOOK S1 John   | Book seat      |
| STATUS S1      | Check seat     |
| CANCEL S1 John | Cancel booking |
| VIEW           | View all seats |

---

Security

SSL/TLS is used to encrypt communication between client and server.

---

How to Run

```bash
python server.py
python client.py
```

---

Performance

* Tested with multiple clients
* Average response time ~100–150 ms
* No race conditions due to thread locking

---

Team

* Server + Logic- https://github.com/pavithrabanvari
* Client + Security- https://github.com/iamleelu27
* Testing + Documentation- 

---
