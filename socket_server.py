# import socket

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server_socket.bind((socket.gethostname(), 12345))

# server_socket.listen()

# client_socket, addr = server_socket.accept()

# while True:
#     message = client_socket.recv(1024).decode()

#     if not message:
#         break


#     list1 = message.split()

#     total_sum = 0

#     for i in list1:
#         total_sum += int(i)

#     client_socket.send(str(total_sum).encode())

# client_socket.close()
# server_socket.close()



import socket

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket_server.bind((socket.gethostname(), 12345))

socket_server.listen()

client_socket, addr = socket_server.accept()

while True:

    message = client_socket.recv(1024).decode()

    if not message or message.lower().strip == "exit":
        break

    numbers = message.split()
    res = 0
    for number in numbers:
        res += int(number)

    client_socket.sendall(str(res).encode())

client_socket.close()
socket_server.close()