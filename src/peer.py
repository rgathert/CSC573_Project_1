import socket
import os
import re
import socket_fun
import multiprocessing as mp


## Initializing all documents to send to server before server connection
# Grabbing documents in RFC/folder

folder_path = './RFC/'
rfc_paths   = {}
rfc_list = ''
if __name__ == '__main__':
    if not os.path.exists(folder_path):
        raise FileNotFoundError("Unable to Find Folder: %s", folder_path)


    # Scanning the RFC folder, and parsing the RFC ID along with the path for said ID
    with os.scandir(folder_path) as it:
        for entry in it:
                entry_name = entry.name
                rfc_id = entry_name.replace('rfc','')
                rfc_id = rfc_id.replace('.txt','')
                rfc_id = int(rfc_id)
                rfc_paths[rfc_id]  = entry.path
                rfc_list = rfc_list + str(rfc_id) + ' '

    # Generating my sockets these sockets will have a seperate process for them
    (p2p_socket, p2p_addr, p2p_port) = socket_fun.p2pRecvSocket()
    client_socket = socket_fun.clientSocket()

    # Creating seperate process for my peer to peer reception socket
    p = mp.Process(target = socket_fun.p2pRecvHandler, args=(p2p_socket,))
    p.daemon = True 
    p.start()
    

    # After booting up p2p socket, set up main server connection

    # TODO: Make Init Message Dynamic
    test_message = f"Hostname: peerA, portNum: {p2p_port}, RFC: {rfc_list}"
    client_socket.send(test_message.encode()) 
    response = client_socket.recv(1024)
    print(f"Server Response {response}")
    client_socket.close()
