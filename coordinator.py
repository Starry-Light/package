import socket
import threading

busy = False
queue = []
lock = threading.Lock()

def handle_client(client,addr):
    global busy

    while True:
        message = client.recv(1024).decode()

        if not message:
            break

        with lock: 
            if message == "REQUEST":
                print(f'REQUEST FROM: {addr}')       
                if not busy:
                    busy = True
                    client.sendall("GRANT".encode())
                    print(f'GRANTED')
                else:
                    print('DEFERRED')
                    queue.append(client)

            elif message == "RELEASE":
                print(f'RELEASED BY ${addr}')
                if queue:
                    next_client = queue.pop(0)
                    next_client.sendall("GRANT".encode())
                    print(f'GRANTED TO ${next_client}')

                else:
                    busy = False

    client.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(), 12345))
server_socket.listen()

print("Coordinator is running...")

while True:
    client_socket, addr = server_socket.accept()
    print(f'Client ${addr} connected to server')
    thread = threading.Thread(
        target=handle_client,
        args=(client_socket,addr)
    )
    thread.start()