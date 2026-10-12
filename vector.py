
import socket
import threading
import sys

ME = int(sys.argv[1])   
N = 3
PORT = 5100 + ME

vector = [0] * N        

def send(pid, msg):
    try:
        s = socket.socket()
        s.connect(("localhost", 5100 + pid))
        s.send(msg.encode())
        s.close()
    except:
        pass

def listener():
    global vector
    server = socket.socket()
    server.bind(("localhost", PORT))
    server.listen(5)
    server.settimeout(1)
    try:
        while True:
            try:
                conn, addr = server.accept()
                sender, values = conn.recv(1024).decode().split("|")
                conn.close()
                received = list(map(int, values.split()))
                for i in range(N):
                    vector[i] = max(vector[i], received[i])   # merge vectors
                vector[ME - 1] += 1                            # receive event
                print("Received from P%s %s -> vector = %s" % (sender, received, vector))
            except socket.timeout:
                pass
    finally:
        server.close()

threading.Thread(target=listener, daemon=True).start()

print("Process", ME, "started (Vector clock)")
print("Commands:  e = internal event   s = send message   q = quit")

try:
    while True:
        cmd = input()

        if cmd == "e":
            vector[ME - 1] += 1                            # internal event
            print("Internal event -> vector = %s" % vector)

        elif cmd == "s":
            pid = int(input("Send to process (1/2/3): "))
            vector[ME - 1] += 1                            # send event
            send(pid, "%d|%s" % (ME, " ".join(map(str, vector))))
            print("Sent to P%d -> vector = %s" % (pid, vector))

        elif cmd == "q":
            break

except KeyboardInterrupt:
    pass


# Vector Clock
# Run in 3 terminals:  python3 vector.py 1
#                      python3 vector.py 2
#                      python3 vector.py 3
