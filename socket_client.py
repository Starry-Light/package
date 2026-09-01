# import socket 

# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# client_socket.connect((socket.gethostname(), 12345))

# while True:

#     message = input("send message to server")

#     if message.lower().strip() != 'exit':
#         client_socket.send(message.encode())

#         data = client_socket.recv(1024).decode()

#         print(data)
#     else:
#         break

# client_socket.close()

import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((socket.gethostname(), 12345))

print("Connected to ", socket.gethostname())

while True:
    message = input("Enter numbers to add: ")
    client_socket.sendall(message.encode())

    if message.lower().strip() == "exit":
        break

    res = client_socket.recv(1024).decode()

    print(f"The sum received is: {res}")

client_socket.close()