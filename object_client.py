import socket
import pickle

class DataObject:
    def __init__(self, name, values):
        self.name = name
        self.values = values

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((socket.gethostname(), 12345))

data_object = DataObject("Student", [10, 20, 30, 40])

serialized_object = pickle.dumps(data_object)

client_socket.sendall(serialized_object)

response = client_socket.recv(4096)

total_sum = pickle.loads(response)

print("Sum received from server:", total_sum)

client_socket.close()