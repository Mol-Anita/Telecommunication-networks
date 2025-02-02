import sys
from socket import AF_INET, SOCK_STREAM, socket
from struct import Struct

hostname = sys.argv[1]
port_number = int(sys.argv[2])
server_address = (hostname, port_number)

packer = Struct("c i")

left_num = 1
right_num = 100

with socket(AF_INET, SOCK_STREAM) as client:
    client.connect(server_address)

    current_number = (left_num + right_num) // 2
    operator = '<'
    packed_data = packer.pack(operator.encode(), current_number)
    client.sendall(packed_data)
    last_operator = '<'

    while True:
        data = packer.unpack(client.recv(packer.size))
        server_response = data[0].decode()
        print(data)

        if server_response in ['K', 'V', 'Y']:
            client.close()
            break

        if left_num >= right_num:
            operator = '='

        if left_num + 1 == right_num:
            operator = '>'

        if last_operator == '>' and server_response == 'I':
            left_num = current_number + 1
        elif last_operator == '<' and server_response == 'I':
            right_num = current_number - 1
        elif last_operator == '>' and server_response == 'N':
            right_num = current_number
        elif last_operator == '<' and server_response == 'N':
            left_num = current_number

        current_number = (left_num + right_num) // 2
        last_operator = operator
        packed_data = packer.pack(operator.encode(), current_number)
        client.sendall(packed_data)
