import socket

SERVER_PORT = 5007
MULTICAST_ADDR = '224.1.1.1'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# allow reuse in case the container restarts quickly
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Listen for clients sending messages to the server
sock.bind(("", SERVER_PORT))

print("Server listening for client messages on UDP port", SERVER_PORT, flush=True)

while True:
    data, addr = sock.recvfrom(1024)

    text = data.decode(errors="ignore")
    print(f"{addr}: {text}", flush=True)

    # Send to multicast group so all clients receive
    sock.sendto(data, (MULTICAST_ADDR, SERVER_PORT))
