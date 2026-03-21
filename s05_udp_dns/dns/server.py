import socket

from dnslib import DNSRecord, QTYPE, RR, A, PTR, RCODE

HOST = "0.0.0.0"
PORT = 53

# Basic DNS mapping (example data)
HOSTS = {
    "example.local": "192.168.100.10",
    "printer.local": "192.168.100.20",
    "router.local": "192.168.100.1",
}

REVERSE = {ip: name for name, ip in HOSTS.items()}


def make_reply(data: bytes) -> bytes:
    try:
        request = DNSRecord.parse(data)
    except Exception:      
        return b""

    reply = request.reply()

    for question in request.questions:
        qname = str(question.get_qname()).rstrip('.')
        qtype = QTYPE[question.qtype]

        if qtype == "A":
            ip = HOSTS.get(qname)
            if ip:
                reply.add_answer(RR(qname, QTYPE.A, rdata=A(ip), ttl=60))
            else:
                reply.header.rcode = RCODE.NXDOMAIN

        elif qtype == "PTR":
            if qname.endswith(".in-addr.arpa"):
                parts = qname.replace(".in-addr.arpa", "").split('.')
                if len(parts) == 4:
                    ip = ".".join(reversed(parts))
                    host = REVERSE.get(ip)
                    if host:
                        reply.add_answer(
                            RR(question.get_qname(), QTYPE.PTR, rdata=PTR(host + "."), ttl=60)
                        )
                    else:
                        reply.header.rcode = RCODE.NXDOMAIN
                else:
                    reply.header.rcode = RCODE.FORMERR
            else:
                reply.header.rcode = RCODE.FORMERR

        else:
            reply.header.rcode = RCODE.NOTIMP

    return reply.pack()


def run_server():
    print(f"Starting DNS UDP server on {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, PORT))
        while True:
            try:
                data, addr = sock.recvfrom(4096)
            except KeyboardInterrupt:
                break
            reply = make_reply(data)
            if reply:
                sock.sendto(reply, addr)


if __name__ == "__main__":
    run_server()
