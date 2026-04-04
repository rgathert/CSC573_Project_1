import socket
import os
import multiprocessing as mp
import sys
from enum_codes import HttpStatus
def p2pRecvSocket():
    p2p_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p2p_socket.bind(('',7736)) # TODO: Use proper port num after testing
    p2p_socket.listen(5) # 5 listeners max
    (address, port) = p2p_socket.getsockname()
    print(f"Peer socket Address: {address}, Port {port}\n")
    return p2p_socket, address, port


# Client socket to connect to server socket
def clientSocket():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost',7734)) #TODO: Get a proper IP, update port to 7734 eventually
    except:
        print(f"Error {HttpStatus.SERVICE_UNAVAILABLE}: Service Unavailable")
        sys.exit(HttpStatus.SERVICE_UNAVAILABLE)
    return client_socket


# Listening to peer socket
def p2pRecvHandler(p2p_socket):
    while True:    
        (peer_connection, peer_address) = p2p_socket.accept()
        p2p_process = mp.Process(target=peerHandling)
        peer_connection.close()

# Setting up server socket connection
def clientSend(client_socket, message_stream):
    # Constructing initial message to send
    client_socket.send(message_stream)


# Handling Peer Connections
def peerHandling():
    # TODO: Adding handing for p2p communication
    return 0



