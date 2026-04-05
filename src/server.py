import socket
import os
import sys
import multiprocessing as mp
import command_handle
from enum_codes import HttpStatus, CommandType, returnPhrase
from server_object import peer, rfc_idx
VERSION_STR = "P2P-CI/1.0"


peer_list = []
rfc_list = []

# Handling server data
def handleData(data, server_connection, client_name, port_num, peer_list, rfc_list):
    
    # Formatting the data into the fields needed
    (command_type, return_code, parsed_data) = command_handle.ServerRequestParse(data, client_name, port_num)
    
    return_phrase = returnPhrase(return_code)
    # Getting status header
    header = f"{VERSION_STR} {return_code.value} {return_phrase}\r\n"

    # Error handling if the status was not OK
    if return_code != HttpStatus.OK:
        server_connection.send(((header + "\r\n")).encode())
        return
    
    if command_type == CommandType.LIST:
        message = command_handle.List(header, rfc_list)
        response = header + "\r\n" + message + "\r\n"
        server_connection.send((response).encode())
        return
    
    if command_type == CommandType.ADD:
        peer_obj = peer(client_name, port_num)

        rfc_num = parsed_data["rfc_num"]
        title = parsed_data["title"]

        rfc_list.append(rfc_idx(rfc_num, title, peer_obj))

        response_body = f"RFC {rfc_num} {title} {client_name} {port_num}\r\n"
        response = header + "\r\n" + response_body + "\r\n"
        server_connection.send(response.encode())
        return
    
    # HTTP Status is OK
    # match command_type:
        
    #     case CommandType.LOOKUP:
    #         return
    #     case CommandType.LIST:
    #         command_handle.List(server_connection, rfc_list)
    #     case CommandType.ADD:
    #         return

    server_connection.send(message.encode())


# Server Socket to Listen to Clients
def serverSocket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost',7734)) #TODO: Get a proper IP
    server_socket.listen(5)
    return server_socket

def clientHandling(server_connection, peer_list: list, rfc_list: list):
    
    # TODO: Make sure we can handle large data fields from the client on startup
    
    
    
    data = server_connection.recv(4096).decode()
    print(f"Raw startup data: {data}\n")
    (client_part, port_part, rfc_part) = data.split(',')
    client_name = client_part.split(': ')[1]
    port_num = int(port_part.split(': ')[1])
    rfc_titles = rfc_part.split(': ')[1].split()
    print(f"Client name: {client_name}, port: {port_num}")
    print(f"RFC titles/raw IDs: {rfc_titles}")
    peer_obj = peer(client_name, port_num)
    peer_list.append(peer_obj)
    
    print(f"Peer list size: {len(peer_list)}") 

    # Creating title object for each rfc title
    for title in rfc_titles:
        rfc_list.append(rfc_idx(title, rfc_num=title, peer_obj=peer_obj))
        print(f"RFC added -> {title} with RFC number {title} from {client_name}")
    
    
    print(f"RFC list size: {len(rfc_list)}")

    server_connection.send(b"REGISTERED")

    print(f"Connection Established")
    
    while True:
        try:
            data = server_connection.recv(4096)
        except ConnectionResetError:
            print(f"Client: {client_name} closed")
            break
        except KeyboardInterrupt:
            print("Client handler shutting down")
            server_connection.close()
        if not data:
            server_connection.close()
            print(f"Client: {client_name} closed")
            break
        data = data.decode()

        print(f"Received command from {client_name}: {data}")

        handleData(data, server_connection, client_name, port_num, peer_list, rfc_list)
         
            


    
    

if __name__ == '__main__':
    manager = mp.Manager()
    # Initialization of global lists for multiprocessing
    peer_list = manager.list()
    rfc_list = manager.list()
    server_socket = serverSocket()

    # Adding in server specific functions not in general function
    # TODO: Make these functions work to be server specific
    try:

        while True:
            (server_connection, server_address) = server_socket.accept()
            server_process = mp.Process(target = clientHandling, args=(server_connection, peer_list, rfc_list))
            # Killing demonic child processes if server closes (lol)
            server_process.daemon = True
            server_process.start()
        
    except KeyboardInterrupt:
        print("Shutting down server...")
        server_socket.close()
        sys.exit(0)