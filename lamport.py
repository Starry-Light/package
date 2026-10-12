
import socket
import threading
import sys

ME = int(sys.argv[1])   
N = 3
PORT = 5000 + ME

clock = 0               

def send(pid, msg):
    try:
        s = socket.socket()
        s.connect(("localhost", 5000 + pid))
        s.send(msg.encode())
        s.close()
    except:
        pass

# Background thread that receives messages from other processes
def listener():
    global clock
    server = socket.socket()
    server.bind(("localhost", PORT))
    server.listen(5)
    server.settimeout(1)
    try:
        while True:
            try:
                conn, addr = server.accept()
                sender, ts = conn.recv(1024).decode().split()
                conn.close()
                clock = max(clock, int(ts)) + 1        # receive rule
                print("Received from P%s (ts=%s) -> clock = %d" % (sender, ts, clock))
            except socket.timeout:
                pass
    finally:
        server.close()

threading.Thread(target=listener, daemon=True).start()

print("Process", ME, "started (Lamport clock)")
print("Commands:  e = internal event   s = send message   q = quit")

try:
    while True:
        cmd = input()

        if cmd == "e":
            clock += 1                                 # internal event
            print("Internal event -> clock = %d" % clock)

        elif cmd == "s":
            pid = int(input("Send to process (1/2/3): "))
            clock += 1                                 # send event
            send(pid, "%d %d" % (ME, clock))
            print("Sent to P%d -> clock = %d" % (pid, clock))

        elif cmd == "q":
            break

except KeyboardInterrupt:
    pass


# Run in 3 terminals:  python3 lamport.py 1
#                      python3 lamport.py 2
#                      python3 lamport.py 3
