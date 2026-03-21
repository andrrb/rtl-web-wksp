import socket

SERVER_PORT = 5007

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# allow reuse in case the container restarts quickly
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Listen for all client broadcast messages
sock.bind(("0.0.0.0", SERVER_PORT))

print("Server listening for client broadcast messages on UDP port", SERVER_PORT, flush=True)

while True:
    data, addr = sock.recvfrom(1024)

    text = data.decode(errors="ignore")
    print(f"{addr}: {text}", flush=True)
