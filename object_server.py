import socket
import pickle

class DataObject:
    def __init__(self, name, values):
        self.name = name
        self.values = values

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((socket.gethostname(), 12345))
server_socket.listen()

print("Server is waiting for a client...")

client_socket, addr = server_socket.accept()
print("Connected to:", addr)

data = client_socket.recv(4096)

received_object = pickle.loads(data)

print("Name:", received_object.name)
print("Values:", received_object.values)

total_sum = sum(received_object.values)

client_socket.sendall(pickle.dumps(total_sum))

client_socket.close()
server_socket.close()