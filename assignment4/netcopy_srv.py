import sys
from socket import socket, AF_INET, SOCK_STREAM
import hashlib

ip = sys.argv[1]
port = int(sys.argv[2])
server_addr = (ip, port)

checksum_srv_ip = sys.argv[3]
checksum_srv_port = int(sys.argv[4])
checksum_server_addr = (checksum_srv_ip, checksum_srv_port)

file_desc = sys.argv[5]
file_path = sys.argv[6]

hash_md5 = hashlib.md5()

with socket(AF_INET, SOCK_STREAM) as server:
    server.bind(server_addr)
    server.listen(1)
    client, client_addr = server.accept()

    data = client.recv(200)
    with open(file_path, "wb") as file:
        while data:
            file.write(data)
            hash_md5.update(data)
            data = client.recv(200)

    client.close()

    with socket(AF_INET, SOCK_STREAM) as checksum_client:
        checksum_client.connect(checksum_server_addr)
        checksum_client.sendall(f"KI|{file_desc}".encode())
        response = checksum_client.recv(200).decode().split("|")

        if response[0] == '0' or response[1] != hash_md5.hexdigest():
            print("CSUM CORRUPTED")
        else:
            print("CSUM OK")
