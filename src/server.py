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
        rfc_title: str
        hostname: str



# Server Socket to Listen to Clients
def serverSocket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost',7734)) #TODO: Get a proper IP
    server_socket.listen(5)
    return server_socket

def clientHandling(server_connection, peer_list, rfc_list):
    
    # TODO: Make sure we can handle large data fields from the client on startup

    data = server_connection.recv(4096).decode()
    (client_part, port_part, rfc_part) = data.split(',')
    client_name = client_part.split(': ')[1]
    port_num = int(port_part.split(': ')[1])
    rfc_title = rfc_part.split(': ')[1].split()

    peer_list.append({"name": client_name, "port": port_num})
    rfc_list.append({"rfc_title": rfc_title, "hostname": client_name})
    
    while True:
        data = server_connection.recv(4096).decode()

        if not data:
            server_connection.close()
            print(f"Client: {client_name} closed")

    
    

if __name__ == '__main__':
    manager = mp.Manager()
    # Initialization of global lists for multiprocessing
    peer_list = manager.list()
    rfc_list = manager.list()
    server_socket = serverSocket()

    # Adding in server specific functions not in general function
    # TODO: Make these functions work to be server specific

    while True:
        (server_connection, server_address) = server_socket.accept()
        server_process = mp.Process(target = clientHandling, args=(server_connection, peer_list, rfc_list))
        # Killing demonic child processes if server closes (lol)
        server_process.daemon = True
        server_process.start()