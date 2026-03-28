import socket
import os
import re
import socket_fun



## Initializing all documents to send to server before server connection
# Grabbing documents in RFC/folder
folder_path = './RFC/'
rfc_paths   = {}
if not os.path.exists(folder_path):
    raise FileNotFoundError("Unable to Find Folder: %s", folder_path)


# Scanning the RFC folder, and parsing the RFC ID along with the path for said ID
with os.scandir(folder_path) as it:
    for entry in it:
            entry_name = entry.name
            rfc_id = re.search(r'\d+',entry_name)
            rfc_paths[int(rfc_id.group())]  = entry.path

# Generating my sockets these sockets will have a seperate process for them
p2p_socket = socket_fun.p2pSocket()
server_socket = socket_fun.serverSocket()

# Creating forks for my peer to peer reception socket
pid = os.fork()
if pid == 0:
    # Generating a fork for one process to listen to p2p socket and 
    # one process to connect to server
    pid = os.fork()
    if pid == 0:
        socket_fun.p2pRecvHandler(p2p_socket)
        os.exit(0)
    else:
        # TODO: Add in server reception
         os.exit(0)
         

