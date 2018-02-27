
import socketserver
import tcplib


class MyTCPHandler(socketserver.StreamRequestHandler):

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        print('{} wrote:'.format(self.client_address[0]))
        parts = self.data.split(' ')
        cliIP = parts[0]
        data = ' '.join(parts[1:])
        answer = None

        if data == 'connection test':
            answer = 'connection test OK'

        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(answer)



if __name__ == '__main__':
    HOST, PORT = 'localhost', 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()