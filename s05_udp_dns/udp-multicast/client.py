import socket
import threading
import sys

SERVER_HOST = 'server'
SERVER_PORT = 5007
MULTICAST_ADDR = '224.1.1.1'

name = sys.argv[1] if len(sys.argv) > 1 else "Anonymous"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# allow reuse
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Always bind so we can receive after joining
sock.bind(("", SERVER_PORT))

joined = False
mreq = socket.inet_aton(MULTICAST_ADDR) + socket.inet_aton('0.0.0.0')


def join_group():
    global joined
    if joined:
        print("Already joined multicast group.")
        return
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    joined = True
    print(f"Joined multicast group {MULTICAST_ADDR} (you will now see chat messages)")


def leave_group():
    global joined
    if not joined:
        print("Not currently joined.")
        return
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
    joined = False
    print("Left multicast group (you will no longer receive chat messages)")


def receive():
    while True:
        data, addr = sock.recvfrom(1024)
        text = data.decode(errors="ignore")
        # ignore our own messages
        if text.startswith(f"{name}:"):
            continue
        if joined:
            print(text)


threading.Thread(target=receive, daemon=True).start()

print(f"Client {name} started. Type /join to subscribe, /leave to unsubscribe, /quit to exit.")

while True:
    try:
        msg = input()
        if msg.strip() == "/join":
            join_group()
            continue
        if msg.strip() == "/leave":
            leave_group()
            continue
        if msg.strip() in ("/quit", "/exit"):
            break
        if not joined:
            print("You are not joined. Use /join to start sending/receiving messages.")
            continue
        sock.sendto(f"{name}: {msg}".encode(), (SERVER_HOST, SERVER_PORT))
    except KeyboardInterrupt:
        break

sock.close()
