import socket
import sys
import multiprocessing as mp
import server_command_handle
from enum_codes import HttpStatus, CommandType, returnPhrase
from server_object import peer, rfc_idx
VERSION_STR = "P2P-CI/1.0"


# Handling server data
def handleData(data, server_connection, client_name, port_num, peer_list, rfc_list):
    
    # Formatting the data into the fields needed
    (command_type, return_code, parsed_data) = server_command_handle.ServerRequestParse(data, client_name, port_num)
    
    return_phrase = returnPhrase(return_code)
    # Getting status header
    header = f"{VERSION_STR} {return_code.value} {return_phrase}\r\n"

    # Error handling if the status was not OK
    if return_code != HttpStatus.OK:
        server_connection.send(((header + "\r\n")).encode())
        return
    
    if parsed_data is None:
        server_connection.send((header + "\r\n").encode())
        return
    
    peer_obj = peer(client_name, port_num)

    if not any((p.host_name == client_name and p.port_num == port_num) for p in peer_list):
        peer_list.append(peer_obj)
    
    if command_type == CommandType.LIST:
        message = server_command_handle.List(header, rfc_list)
        
        server_connection.send(message.encode())
        return
    
    if command_type == CommandType.ADD:
        
        rfc_num = parsed_data["rfc_num"]
        title = parsed_data["title"]

        response = server_command_handle.Add(header, rfc_num, title, peer_obj, rfc_list)
        
        server_connection.send(response.encode())
        return
    
    if command_type == CommandType.LOOKUP:
        rfc_num = parsed_data["rfc_num"]
        response = server_command_handle.Lookup(header, rfc_num, rfc_list)
        if response is None:
            not_found_header = f"{VERSION_STR} {HttpStatus.NOT_FOUND.value} {returnPhrase(HttpStatus.NOT_FOUND)}\r\n\r\n"
            server_connection.send(not_found_header.encode())
        else:
            server_connection.send(response.encode())
        return
    



# Server Socket to Listen to Clients
def serverSocket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('',7734)) 
    server_socket.listen(5)
    print("Listening on port 7734\n")
    return server_socket


def clientHandling(server_connection, peer_list, rfc_list):
    print("Connection Established ")

    current_peer_name = None
    current_peer_port = None

    try:
        while True:
            data = server_connection.recv(4096)
            if not data:
                break

            decoded = data.decode()
            print(f"Received command from connection: {decoded}")

            command_lines = decoded.split('\r\n')
            if len(command_lines) >= 3:
                host_header = command_lines[1].split(' ')
                port_header = command_lines[2].split(' ')
                if len(host_header) > 1 and len(port_header) > 1:
                    current_peer_name = host_header[1]
                    current_peer_port = int(port_header[1])

            handleData(decoded, server_connection, current_peer_name, current_peer_port, peer_list, rfc_list)

    except ConnectionResetError:
        pass
    finally:
        server_connection.close()

        if current_peer_name is not None and current_peer_port is not None:
            for i in range(len(rfc_list) - 1, -1, -1):
                if rfc_list[i].host_name == current_peer_name and rfc_list[i].port_num == current_peer_port:
                    del rfc_list[i]

            for i in range(len(peer_list) - 1, -1, -1):
                if peer_list[i].host_name == current_peer_name and peer_list[i].port_num == current_peer_port:
                    del peer_list[i]


    
    

if __name__ == '__main__':
    manager = mp.Manager()
    # Initialization of global lists for multiprocessing
    peer_list = manager.list()
    rfc_list = manager.list()
    server_socket = serverSocket()
    print("Server Started\n")

    # Adding in server specific functions not in general function
    try:

        while True:
            (server_connection, server_address) = server_socket.accept()
            server_process = mp.Process(target = clientHandling, args=(server_connection, peer_list, rfc_list))
            # Killing demonic child processes if server closes (lol)
            server_process.daemon = True
            server_process.start()
        
    except KeyboardInterrupt:
        print("Stopping server\n")
        server_socket.close()
        sys.exit(0)