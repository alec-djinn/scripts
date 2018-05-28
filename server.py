# server.py

import socket

                   

host = 'localhost'
port = 60000

with socket.socket() as s:
    s.bind((host, port))            # Bind to the port
    s.listen(5)                     # Now wait for client connection.
    print('Server listening....')
    while True:
        conn, addr = s.accept()
        print('Got connection from', addr)
        data = conn.recv(1024)
        print('Server received', repr(data))
        #instructions = parse(data)
        #stout, sterr, msg = execute(instuctions)
        #conn.send(msg)
        msg = 'server_message'
        conn.send(msg.encode('utf-8'))