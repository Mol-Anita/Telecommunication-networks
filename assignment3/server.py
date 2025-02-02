import random
import sys
from socket import socket, AF_INET, SOCK_STREAM
from struct import Struct
from select import select

hostname = sys.argv[1]
port_number = int(sys.argv[2])
server_address = (hostname, port_number)

packer = Struct("c i")

number_to_guess = random.randint(1, 100)

with socket(AF_INET, SOCK_STREAM) as server:
    inputs = [server]
    outputs = []
    timeout = 1

    server.bind(server_address)
    server.listen(5)
    over = False
    while True:
        readable, writeable, exceptions = select(inputs, inputs, inputs, timeout)

        if not (readable or writeable or exceptions):
            continue

        for s in readable:
            if s is server:
                client, client_address = server.accept()
                inputs.append(client)
            else:
                data = s.recv(packer.size)
                if not data:
                    inputs.remove(s)
                    s.close()
                else:
                    print(packer.unpack(data))
                    operator, number = packer.unpack(data)
                    operator = operator.decode()

                    response_data = ''
                    if over:
                        response_data = packer.pack('V'.encode(), 0)

                    elif operator == "=":
                        if number == number_to_guess:
                            over = True
                            response_data = packer.pack('Y'.encode(), 0)
                        else:
                            response_data = packer.pack('K'.encode(), 0)

                    elif operator == ">":
                        if number < number_to_guess:
                            response_data = packer.pack('I'.encode(), 0)
                        else:
                            response_data = packer.pack('N'.encode(), 0)

                    elif operator == "<":
                        if number > number_to_guess:
                            response_data = packer.pack('I'.encode(), 0)
                        else:
                            response_data = packer.pack('N'.encode(), 0)
                    s.sendall(response_data)
