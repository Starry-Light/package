import socket
import threading
import sys
import time

PORTS = [6000, 6001, 6002]
TOTAL_PROCESSES = 3

process_id = int(sys.argv[1])
my_port = PORTS[process_id]

clock = 0
state = "RELEASED"
request_time = 0

replies = set()
deferred = []

lock = threading.Lock()
condition = threading.Condition(lock)

def send_message(target_id, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(("localhost", PORTS[target_id]))
    client_socket.sendall(message.encode())

    client_socket.close()

def handle_request(timestamp, sender_id):
    global clock

    with lock:
        clock = max(clock, timestamp) + 1

        should_defer = (
            state == "HELD" or
            (
                state == "WANTED" and
                (request_time, process_id) < (timestamp, sender_id)
            )
        )

        if should_defer:
            deferred.append(sender_id)
        else:
            send_message(sender_id, f"REPLY {process_id}")

def handle_reply(sender_id):
    with condition:
        replies.add(sender_id)
        condition.notify()

def receive_messages():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", my_port))
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        message = client_socket.recv(1024).decode()
        client_socket.close()

        parts = message.split()

        if parts[0] == "REQUEST":
            handle_request(int(parts[1]), int(parts[2]))

        elif parts[0] == "REPLY":
            handle_reply(int(parts[1]))

thread = threading.Thread(target=receive_messages)
thread.daemon = True
thread.start()

time.sleep(1)

while True:
    choice = input("Type request to enter CS, or exit: ")

    if choice.lower() == "exit":
        break

    if choice.lower() == "request":
        with condition:
            clock += 1
            request_time = clock
            state = "WANTED"
            replies.clear()

        print("Process", process_id, "is requesting critical section")

        for i in range(TOTAL_PROCESSES):
            if i != process_id:
                send_message(i, f"REQUEST {request_time} {process_id}")

        with condition:
            while len(replies) < TOTAL_PROCESSES - 1:
                condition.wait()

            state = "HELD"

        print("Process", process_id, "entered critical section")
        time.sleep(3)
        print("Process", process_id, "left critical section")

        with lock:
            state = "RELEASED"

            for waiting_process in deferred:
                send_message(waiting_process, f"REPLY {process_id}")

            deferred.clear()