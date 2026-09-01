import socket
import threading

def receive_messages():
    while True:
        message = client_socket.recv(1024).decode()

        if not message:
            break

        print("\nMessage:", message)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((socket.gethostname(), 12345))

thread = threading.Thread(target=receive_messages)
thread.start()

while True:
    message = input()

    if message.lower() == "exit":
        break

    client_socket.sendall(message.encode())

client_socket.close()