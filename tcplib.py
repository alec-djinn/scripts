import sys
import socket



## Helper functions
def getMyIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    myIP = s.getsockname()[0]
    s.close()
    return myIP



## Commands
def help(doc):
    print(doc)

def send(ip, port, data, myIP=getMyIP()):
    received = None
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(bytes(f'{myIP} {data}\n', 'utf-8'))
        # Receive data from the server and shut down
        received = str(sock.recv(1024), 'utf-8')
    print(f'Sent:     {data}')
    print(f'Received: {received}')

def test(ip, port, myIP):
    data = 'connection test'
    send(ip, port, data, myIP)
    