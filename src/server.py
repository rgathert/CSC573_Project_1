import socket
import os
import sys
import multiprocessing as mp
import command_handle
from enum_codes import HttpStatus, CommandType, returnPhrase

VERSION_STR = "P2P-Cl/1.0"

# Creating a peer object (has hostname, and port value)
class peer:
    def __init__(self, host_name, port_num):
        self.host_name = host_name
        self.port_num = port_num

class rfc_idx:
    def __init__(self, title, peer_type):
        self.title = title
        self.peer = peer_type
peer_list = []
rfc_list = []

# Handling server data
def handleData(data, server_connection, client_name, port_num, peer_list, rfc_list):

    # Formatting the data into the fields needed
    (command_type, return_code) = command_handle.ServerRequestParse(data, client_name, port_num)
    
    return_phrase = returnPhrase(return_code)
    # Getting status header
    message = f"{VERSION_STR} {return_code} {return_phrase}\r\n"

    # Error handling if the status was not OK
    if return_code != HttpStatus.OK:
        server_connection.send(message.encode())
        return
    # HTTP Status is OK
    match command_type:
        
        case CommandType.LOOKUP:
            return
        case CommandType.LIST:
            command_handle.List(server_connection, rfc_list)
            return
        case CommandType.ADD:
            return


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

    peer_obj = peer(client_name, port_num)
    peer_list.append(peer_obj)

    rfc_list.append(rfc_idx(rfc_title, peer_obj))
    
    while True:
        data = server_connection.recv(4096).decode()

        if not data:
            server_connection.close()
            print(f"Client: {client_name} closed")
            return 0
        
        handle_data(data, server_connection, client_name, port_num)
         
            


    
    

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