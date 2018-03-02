
import socketserver
import tcplib
import os
import sys
import time
import random


ver = '0.1'

class MyTCPHandler(socketserver.StreamRequestHandler):

    def answer(self, message):
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        try:
            self.wfile.write(message.encode('utf-8'))
            print('answer sent')
        except Exception as e:
            print(e)

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().decode('utf-8').strip()
        parts = self.data.split(' ')
        cliIP = parts[0]
        data = ' '.join(parts[1:])
        msg = 'OK'
        print(f'{self.client_address[0]}@{cliIP} wrote: {data[:50]}...')

        
        if data == 'connection test':
            msg = 'connection established, all OK'

        elif data.strip() == 'restart!':
            msg = 'restarting server...'
            self.answer(msg)
            os.execl(sys.executable, *([sys.executable]+sys.argv))

        elif parts[1] == 'txt':
            filename = parts[2]
            with open('new_file.txt', 'w') as out:
                for line in self.data.split('_*_')[1:]:
                    out.write(f'{line}\n')
            msg = 'file uploaded'

        elif parts[1] == 'me':
            filename = parts[2]
            with open(filename, 'w') as out:
                for line in self.data.split('_*_')[1:]:
                    out.write(f'{line}\n')
            msg = 'file uploaded'

        self.answer(msg)
 

        


if __name__ == '__main__':

    HOST, PORT = 'localhost', 9999

    attempts = 0
    while True:

        ###############################################################
        ## Connect to other ports if the standard one is not working ##
        attempts += 1
        if attempts > 10:
            if random.randint(0,1):
                #try a restricted subset of ports
                PORT = random.sample(range(1111,9999,1111),1)[0]
            else:
                #try a random port
                PORT = random.randint(1,65535)
        if attempts > 100:
            #try again with the standard port
            attempts = 0
        ###############################################################

        try:
            print(f'TCP-SRV {ver} :::powered by TCPLIB {tcplib.ver}:::')
            # Create the server, binding to localhost on port 9999
            server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            server.serve_forever()
        except OSError as e:
            print(e)
            print('waithing for a few seconds before trying again...')
            time.sleep(random.randint(1,10))
        
    