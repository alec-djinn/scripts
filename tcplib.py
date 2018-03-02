import sys
import socket
import random
import pickle

ver = '0.1'

## Helper functions
def connect():
    pass


def sendFile(infile, socket):
    while True:
        conn, addr = socket.accept()     # Establish connection with client.
        print('Got connection from', addr)
        data = conn.recv(1024)
        print('Server received', repr(data))

        with open(infile,'rb') as f:
            l = f.read(1024)
            while (l):
               conn.send(l)
               print('Sent ',repr(l))
               l = f.read(1024)

            print('Done sending')
            conn.send('Thank you for connecting'.encode('utf-8'))
            conn.close()
    print('Server listening....')


def receiveFile(outfile, socket):
    with open(outfile, 'wb') as f:
        print('file opened')
        while True:
            print('receiving data...')
            data = socket.recv(1024)
            print(f'{data}')
            if not data:
                break
            # write data to a file
            f.write(data)
    print('file received')