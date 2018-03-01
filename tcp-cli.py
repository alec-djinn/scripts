import sys
import socket
import tcplib


## Docs
ver  = '0.1'
req  = 'Python >= 3.6'
doc  = \
f'''
TCP-CLI {ver}. :::powered by TCPLIB {tcplib.ver}:::

requirements: {req}
       usage: python tcp-cly.py <command> <arguments>

COMMAND                        ARGUMENTS                        DESCRIPTION

help                           ...                              print this doc
--------------
askfor                         <ip> <port> <object>             ask the server for a specific object, receive a pickle.dumps() or None
defaults                       ...                              print the list of defautl addresses
pullme                         <ip> <port>                      download a copy of itself from the remote host
pushme                         <ip> <port>                      send a copy of itself to the remote host
send                           <ip> <port> <string>             send a message (see [1])
sendencrypt                    <ip> <port> <string>             send an encrypted message
sendfile                       <ip> <port> <path>               send a file
sendpickle                     <ip> <port> <path>               send a pickle.dump() file
test                           <ip> <port>                      run a connection test
--------------


NOTES

[0] If <ip> and <port> are not passed as arguments, default values will be used instead.
    The current list of default addresses can be printed on screen by using: defaults.
    You can use the option -dN, where N is an integer, to specify a default address.
    If nothing is passd, then -d0 (the first available default address) is used by default.
    In extreme cases, a random address will be chosen.

[1] Special messages, followed by '!' and can be parsed and executed by the server.
    Example: <send ip port restart!> will force the server to restart. 
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



## help
if cmd == 'help':
    tcplib.help(doc)
    sys.exit()


elif cmd == 'send':
    myIP = tcplib.getMyIP()
    ip, port = tcplib.getAddress(args)
    data = ' '.join(args[2:])
    try:
        tcplib.send(ip, port, data, myIP)
    except Exception as e:
        print(e)


elif cmd == 'sendfile':
    myIP = tcplib.getMyIP()
    ip, port = tcplib.getAddress(args)
    filepath = ' '.join(args[2:])
    try:
        tcplib.sendfile(ip, port, filepath, myIP)
    except Exception as e:
        print(e)


## defaults
elif cmd == 'defaults':
    print(tcplib.defaults)


## test
elif cmd == 'test':
    myIP = tcplib.getMyIP()
    ip, port = tcplib.getAddress(args)
    print(f'testing connection to {ip}:{port}')
    try:
        tcplib.test(ip, port, myIP)
    except Exception as e:
        print(e)

















