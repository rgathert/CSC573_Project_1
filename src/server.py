import socket
import os
import sys
import multiprocessing as mp


# Creating a peer object (has hostname, and port value)
class peer:
    def __init__(self, host_name, port_num):
        host_name: str
        port_num: int

class rfc_idx:
    def __init__(self, num, title, hostname):
        num: int
        title: str
        hostname: str

# Initialization of lists
peer_list = []
rfc_list = []

# Server Socket to Listen to Clients
def serverSocket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost',7734)) #TODO: Get a proper IP
    server_socket.listen(5)
    return server_socket

def clientHandling(server_connection, peer_list, rfc_list):
    print("Peer_Conn_test")
    data = server_connection.recv(1024).decode()

    (client_part, port_part, rfc_part) = data.split(',')

    client_name = client_part.split(': ')[1]
    port_num = int(port_part.split(': ')[1])
    rfc_id = rfc_part.split(': ')[1].split()

    
    server_connection.close()
    

if __name__ == '__main__':


    

    server_socket = serverSocket()


    # Adding in server specific functions not in general function
    # TODO: Make these functions work to be server specific

    while True:
        (server_connection, server_address) = server_socket.accept()
        server_process = mp.Process(target = clientHandling, args=(server_connection, peer_list, rfc_list))
        server_process.daemon = True
        server_process.start()