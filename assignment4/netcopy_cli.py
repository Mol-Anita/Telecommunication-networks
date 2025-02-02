import hashlib
import sys
from socket import socket, AF_INET, SOCK_STREAM

srv_ip = sys.argv[1]
srv_port = int(sys.argv[2])
server_addr = (srv_ip, srv_port)

checksum_srv_ip = sys.argv[3]
checksum_srv_port = int(sys.argv[4])
checksum_server_addr = (checksum_srv_ip, checksum_srv_port)

file_desc = sys.argv[5]
file_path = sys.argv[6]

hash_md5 = hashlib.md5()

with socket(AF_INET, SOCK_STREAM) as client:
    client.connect(server_addr)
    with open(file_path, "rb") as file:
        for line in file.readlines():
            client.sendall(line)
            hash_md5.update(line)

data = f"BE|{str(file_desc)}|60|{str(len(hash_md5.hexdigest()))}|{hash_md5.hexdigest()}"
with socket(AF_INET, SOCK_STREAM) as client:
    client.connect(checksum_server_addr)
    client.sendall(data.encode())
    response = client.recv(10)
    print("Checksum server response:", response.decode())
