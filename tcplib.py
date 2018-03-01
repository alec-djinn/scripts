import sys
import socket
import random

ver = '0.1'

## Helper functions
def getMyIP():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.connect(("8.8.8.8", 80))
        myIP = sock.getsockname()[0]
    return myIP


def getAddress(args):
    if len(args):
        ip   = args[0]
        port = args[1]
    else:
        ip, port = getRndDefault()
    return ip, port
    

def getRndDefault():
    r = [line.split() for line in defaults.split('\n') if line != '']
    return random.sample(r, 1)[0]


## Globals
defaults = \
'''
45.32.234.72 9999
'''

## Commands
def help(doc):
    print(doc)


def send(ip, port, data, myIP):
    received = None
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((ip, int(port)))
        sock.sendall(bytes(f'{myIP} {data}\n', 'utf-8'))
        # Receive data from the server and shut down
        received = str(sock.recv(1024), 'utf-8')
    print(f'Sent:     {data}')
    print(f'Received: {received}')


def sendfile(ip, port, filepath, myIP):
    tag = 'txt'
    file_content = ''
    with open(filepath, 'r') as f:
        for line in f:
            file_content += f'_*_{line.strip()}'
    data = f'{tag} {file_content}'
    send(ip, port, data, myIP)



def test(ip, port, myIP):
    data = 'connection test'
    send(ip, port, data, myIP)


    