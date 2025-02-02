from socket import socket, AF_INET, SOCK_STREAM
from select import select
import sys

ADD = "BE"
GET = "KI"

ip = sys.argv[1]
port = int(sys.argv[2])
server_addr = (ip, port)

checksum_database = {}

with socket(AF_INET, SOCK_STREAM) as checksum_srv:
    checksum_srv.bind(server_addr)

    inputs = [checksum_srv]
    timeout = 1
    checksum_srv.listen(5)

    while True:
        rd, wr, ex = select(inputs, inputs, inputs, timeout)

        if not (rd or wr or ex):
            continue

        for s in rd:
            if s is checksum_srv:
                client, client_addr = s.accept()
                inputs.append(client)
                print("Connected:", client_addr)

            else:
                data = s.recv(200)
                if not data:
                    print("Disconnected:", s.getpeername())
                    inputs.remove(s)
                    s.close()

                else:
                    data = data.decode().split("|")
                    if data[0] == ADD:
                        file_desc, valid_time, checksum_len, checksum = data[1:]
                        checksum_database[file_desc] = (checksum_len, checksum)
                        s.sendall("OK".encode())

                    elif data[0] == GET:
                        file_desc = data[1]
                        if file_desc in checksum_database:
                            s.sendall(f"{checksum_database[file_desc][0]}|{checksum_database[file_desc][1]}".encode())
                        else:
                            s.sendall("0|".encode())
