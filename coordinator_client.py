import socket
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((socket.gethostname(), 12345))

print("Requesting critical section...")
client_socket.sendall("REQUEST".encode())

message = client_socket.recv(1024).decode()

if message == "GRANT":
    print("Permission granted. Entering critical section...")

    time.sleep(5)

    print("Leaving critical section...")
    client_socket.sendall("RELEASE".encode())

client_socket.close()