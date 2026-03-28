import socket
import os

def p2pRecvSocket():
    p2p_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p2p_socket = p2p_socket.bind(('',0))
    p2p_socket.listen(5) # 5 listeners max
    return p2p_socket


# Connection to server socket
def serverSocket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(('Localhost',7734)) #TODO: Get a proper IP
    return server_socket


# Listening to peer socket
def p2pRecvHandler(p2p_socket):
    while True:    
        p2p_socket.accept()
        pid = os.fork()
        if pid == 0:
            # TODO: Add in logic for when a connection is recieved on socket
            os.exit(0)
    conn.close()



