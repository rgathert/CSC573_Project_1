import socket
import os
import re

# Grabbing documents in RFC/folder
folder_path = './RFC/'
rfc_paths   = {}
if not os.path.exists(folder_path):
    raise FileNotFoundError("Unable to Find Folder: %s", folder_path)

idx = 0

# Scanning the RFC folder, and parsing the RFC ID along with the path for said ID
with os.scandir(folder_path) as it:
    for entry in it:
            entry_name      = entry.name
            rfc_id          = re.search(r'\d+',entry_name)
            rfc_paths[int(rfc_id.group())]  = entry.path
            
    
print("RFC_map:", (rfc_paths))




# Connecting to the server socket
#peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#peer_socket.connect(('Localhost',7734)) #TODO: Get a proper IP




