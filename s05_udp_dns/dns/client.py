import socket
import os

from dnslib import DNSRecord, QTYPE, RCODE

HOST = os.environ.get("DNS_SERVER_HOST", "server")
PORT = int(os.environ.get("DNS_SERVER_PORT", "53"))


def dns_query(name: str, qtype: str) -> str:
    q = DNSRecord.question(name, qtype)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(5)
        sock.sendto(q.pack(), (HOST, PORT))
        data, _ = sock.recvfrom(4096)

    reply = DNSRecord.parse(data)
    if reply.header.rcode != 0:
        return f"ERROR {RCODE[reply.header.rcode]}"

    if not reply.rr:
        return "(no answers)"

    return "\n".join(str(r) for r in reply.rr)


def reverse_ip(ip: str) -> str:
    parts = ip.strip().split('.')
    if len(parts) != 4:
        raise ValueError("Invalid IPv4 address")
    return ".".join(reversed(parts)) + ".in-addr.arpa"


def prompt():
    print("DNS UDP Client")
    print("Commands:")
    print("  1 - lookup hostname -> IP (A record)")
    print("  2 - lookup IP -> hostname (PTR record)")
    print("  0 - exit")

    while True:
        try:
            choice = input("Choice: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye")
            break
        if choice == "0":
            break
        if choice == "1":
            name = input("Hostname: ").strip()
            if not name:
                continue
            try:
                print(dns_query(name, "A"))
            except Exception as e:
                print("Error:", e)
            continue
        if choice == "2":
            ip = input("IP: ").strip()
            if not ip:
                continue
            try:
                rev = reverse_ip(ip)
                print(dns_query(rev, "PTR"))
            except Exception as e:
                print("Error:", e)
            continue
        print("Unknown choice")


if __name__ == "__main__":
    prompt()
