import socket
import struct

NAME="Короткий Фёдор\n"

def receive_token_and_port():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.settimeout(1)
    conn.connect(("127.0.0.1", 8080))
    conn.sendall(NAME.encode("utf-8"))

    line = b""
    while True:
        if len(line) > 1024:
            raise ValueError("Token is too long")

        buf = conn.recv(1024)
        lines = buf.split(b"\n")
        line += lines[0]

        if len(lines) > 1:
            break

    port, token = line.split(b" ", 1)
    port = int(port.decode('utf-8'))
    if port >= 65536 or port < 0:
        raise ValueError("Invalid port: %s" % str(port))
    return port, token

def read_msg(sock):
    l = struct.unpack("i", conn.recvall(4))
    if l < 0 or l > 4096:
        raise ValueError("Invalid len: %d" % l)
    return conn.recvall(l)

def send_msg(sock, msg):
    conn.sendall(struct.pack("i", len(msg)))
    conn.sendall(msg)

def handshake(port, token):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.settimeout(1)
    conn.connect(("127.0.0.1", port))

    send_msg(sock, msg)

    expr = read_msg(sock).decode("utf-8")
    a, b = expr.split("*")
    с = int(a) * int(b)
    c = str(c).encode("utf-8")
    send_msg(sock, c)

    flag = read_msg(sock).decode("utf-8")
    return flag

def retry(fn, times):
    for i in range(times):
        try:
            return fn()
        except Exception as e:
            print("Fail:", e)
            if i == times - 1:
                raise

def main():
    port, token = retry(lambda: receive_token_and_port(), 5)
    flag = retry(lambda: handshake(port, token), 5)

    print("All done")
    print(flag)

if __name__ == "__main__":
    main()
