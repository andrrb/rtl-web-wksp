import socket
import threading
import sys

SERVER_PORT = 5007
BROADCAST_ADDR = '255.255.255.255'
# Broadcast port is the same as server port (all clients listen/send on the same port)

name = sys.argv[1] if len(sys.argv) > 1 else "Anonymous"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# bind so we can receive broadcast packets
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# allow broadcasting
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind(("0.0.0.0", SERVER_PORT))  # listen for broadcast messages


def receive():
    while True:
        data, addr = sock.recvfrom(1024)
        text = data.decode(errors="ignore")
        # ignore our own messages
        if text.startswith(f"{name}:"):
            continue
        print(text)


threading.Thread(target=receive, daemon=True).start()

print(f"Client {name} joined the chat. Type messages to send.")

while True:
    try:
        msg = input()
        sock.sendto(f"{name}: {msg}".encode(), (BROADCAST_ADDR, SERVER_PORT))
    except KeyboardInterrupt:
        break

sock.close()
