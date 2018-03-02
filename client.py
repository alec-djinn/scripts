# client.py

import socket

             
host = 'localhost'
port = 60000




with socket.socket() as s:
    s.connect((host, port))
    msg = 'client_message'
    s.send(msg.encode('utf-8'))
    rsp = s.recv(1024)
    print(rsp)




