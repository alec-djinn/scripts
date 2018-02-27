import sys
import socket
import tcplib


## Docs
ver  = 'Alpha'
req  = 'Python >= 3.6'
doc  = \
f'''
TCP-CLI version {ver}. Requires {req}.

usage: python tcp-cly.py <command> <arguments>

COMMAND                        ARGUMENTS                        DESCRIPTION

help                           ...                              show this doc 
test                           <ip> <port>                      run a connection test
send                           <ip> <port> <string>             send a message
sendencrypt                    <ip> <port> <string>             send an encrypted message
sendfile                       <ip> <port> <path>               send a file
sendpickle                     <ip> <port> <path>               send a pickle.dump() file
askfor                         <ip> <port> <object>             ask the server for a specific object, receive a pickle.dumps() or None
update                         ...                              check for updates, ask before installing
'''


## Agrs parsing
try:
    cmd  = sys.argv[1]
    args = sys.argv[2:]
    assert cmd in dir(tcplib)
except IndexError:
    err_msg = f'TCP-CLI err: no arguments passed, you must puss at least one.'
    tip_msg = f'TCP-CLI tip: try "python tcp-cly.py help"'
    print(err_msg)
    print(tip_msg)
    sys.exit()
except AssertionError:
    err_msg = f'TCP-CLI err: {cmd} is not a valid command'
    tip_msg = f'TCP-CLI tip: try "python tcp-cly.py help"'
    print(err_msg)
    print(tip_msg)
    sys.exit()
########


## Init
HOST, PORT = 'localhost', 9999
myIP = tcplib.getMyIP()
########



if cmd == 'help':
    tcplib.help(doc)
    sys.exit()

elif cmd == 'test':
    if len(args):
        ip   = args[0]
        port = args[1]
    else:
        ip   = HOST
        port = PORT
    tcplib.test(HOST, PORT, myIP)














