import socket
import threading
import sys
import time

PORTS = [5000, 5001, 5002]

process_id = int(sys.argv[1])
my_port = PORTS[process_id]
next_process = (process_id + 1) % 3
next_port = PORTS[next_process]

token_event = threading.Event()

def receive_token():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", my_port))
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        message = client_socket.recv(1024).decode()

        if message == "TOKEN":
            print("Process", process_id, "received token")
            token_event.set()

        client_socket.close()

def send_token():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", next_port))
    client_socket.sendall("TOKEN".encode())
    client_socket.close()

thread = threading.Thread(target=receive_token)
thread.daemon = True
thread.start()

time.sleep(1)

if process_id == 0:
    print("Process 0 starts with token")
    token_event.set()

while True:
    print("Process", process_id, "is waiting for token...")
    token_event.wait()
    token_event.clear()

    choice = input("Enter critical section? (y/n): ")

    if choice.lower() == "y":
        print("Process", process_id, "entered critical section")
        time.sleep(3)
        print("Process", process_id, "left critical section")

    print("Process", process_id, "sending token to", next_process)
    send_token()