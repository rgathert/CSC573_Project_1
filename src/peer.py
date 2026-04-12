import socket
import os
import re
import socket_fun
import multiprocessing as mp
import peer_command_handle
import sys
## Initializing all documents to send to server before server connection
# Grabbing documents in RFC/folder

folder_path = './RFC/'
rfc_list = ''
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: peer.py <peer_name>")
        sys.exit(1)

    host_name = sys.argv[1]
    host_name = 'localhost'
    if not os.path.exists(folder_path):
        raise FileNotFoundError("Unable to Find Folder: %s", folder_path)

    manager = mp.Manager()
    rfc_paths = manager.dict()

    

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
    p = mp.Process(target = socket_fun.p2pRecvHandler, args=(p2p_socket, rfc_paths, host_name))
    p.daemon = True 
    p.start()
    

    # After booting up p2p socket, set up main server connection
    print(f"Local RFC list: {rfc_list}")
    print(f"Connecting to server...")
    # TODO: Make Init Message Dynamic
    test_message = f"Hostname: {host_name}, portNum: {p2p_port}, RFC: {rfc_list}"
    print(f"Sending startup message: {test_message}")
    client_socket.send(test_message.encode()) 
    
    response = client_socket.recv(1024)
    print(f"Server Response {response}")
    # client_socket.close()
    #TODO: See if there is something else we can do besides the try catch
    try:
        while True:
            arg_in = input("Type 'quit' to exit: ").strip()
            if not arg_in:
                continue
            args = arg_in.split()
            cmd = args[0].lower()

            if cmd == "quit":
                break

            elif cmd == "list":
                peer_command_handle.listRequest(host_name, p2p_port, client_socket)

            elif cmd == "add":
                rfc_num = input("RFC number: ").strip()
                data = peer_command_handle.addRequest(rfc_num, host_name, p2p_port, client_socket, rfc_paths)  

            elif cmd == "get":

                if len(args) != 4:
                    print("Usage: GET <rfc_num> <peer_host> <peer_port>")
                    continue

                rfc_type = args[1]
                peer_host = args[2]

                try:
                    peer_port = int(args[3])
                except:
                    print("peer_port must be an integer")
                    continue
                peer_get_socket = socket_fun.p2pSendHandler(peer_host, peer_port)
                if peer_get_socket is None:
                    continue
                msg = peer_command_handle.getRequest(rfc_type, peer_host)
                peer_get_socket.send(msg.encode())
                return_code = socket_fun.fileRecvHandler(peer_get_socket, rfc_type)

                if(return_code != 0):
                    print("Error During file transfer, please try again")
                        

            else:
                print(f"Usage: \r\n"
                      "LIST: List all RFC's reachable with the connected server\r\n"
                      "ADD: Add a new RFC to the servers database\r\n"
                      "GET <rfc_num> <peer_host> <peer_port>: Download a new RFC from a peer\r\n")

    finally:
        # Closing off the sockets
        p2p_socket.close()
        client_socket.close()