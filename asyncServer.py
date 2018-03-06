import asyncore

class Handler(asyncore.dispatcher):
    def __init__(self, sock):
        self.buffer = b''
        super().__init__(sock)

    def handle_read(self):
        self.buffer += self.recv(4096)
        print('current buffer: %r' % self.buffer)


class Server(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accepted(self, sock, addr):
        print('Incoming connection from %s' % repr(addr))
        Handler(sock)


if __name__ == "__main__":
    server = Server("localhost", 1234)
    asyncore.loop()
