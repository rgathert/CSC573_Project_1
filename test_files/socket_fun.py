import socket
import os
import multiprocessing as mp
import sys
import peer_command_handle
from enum_codes import HttpStatus, returnPhrase, CommandType


#TODO: Find way to abstract this
VERSION_STR = "P2P-CI/1.0"

def p2pRecvSocket():
    p2p_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p2p_socket.bind(('',0)) # TODO: Use proper port num after testing
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
        print(f"Error {HttpStatus.SERVICE_UNAVAILABLE.value}: Service Unavailable")
        sys.exit(HttpStatus.SERVICE_UNAVAILABLE.value)
    return client_socket


# Listening to peer socket, and handling get request from a peer
def p2pRecvHandler(p2p_socket, rfc_index, host_name):
    while True:
        
        #TODO: See if we want a better way to leave? Maybe after quitting
        try:
            (peer_connection, peer_address) = p2p_socket.accept()
        except KeyboardInterrupt:
            break
        
        data = peer_connection.recv(4096).decode()

        #TODO: Remove this test print later
        print(f"Recieved request from {peer_address}")
        
        (command_type, return_code, parsed_request) = peer_command_handle.PeerRequestParse(data, host_name)
        
        header = f"{VERSION_STR} {return_code.value} {returnPhrase(return_code)}\r\n"
        if return_code != HttpStatus.OK:
            peer_connection.send(((header + "\r\n")).encode())
            peer_connection.close()
            continue
        
        rfc_num = parsed_request["rfc_val"]
        if rfc_num not in rfc_index:
            header = f"{VERSION_STR} {return_code.value} {returnPhrase(return_code.value)}"
            peer_connection.send(((header + "\r\n")).encode())
            peer_connection.close()
            continue

        header = f"{VERSION_STR} {HttpStatus.OK.value} {returnPhrase(HttpStatus.OK)}\r\n"
        peer_connection.sendall(peer_command_handle.fileSend(header, rfc_index[rfc_num]).encode())
        peer_connection.close()
        
        
        
        
# Setting up server socket connection
def clientSend(client_socket, message_stream):
    # Constructing initial message to send
    client_socket.send(message_stream)


# Handling Peer GET Transmission
def p2pSendHandler(peer_host, peer_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((peer_host, peer_port))
        return sock
    except:
        #TODO Get a better error handling message here from HTTP codes
        print(f"Error 503 - Service Unavailable")
        sock.close()
        return None


def fileRecvHandler(recv_socket, rfc_num):

    # Starting out with bytestream then will do conversion later
    buffer =  b""
    
    # Reading chunks at a time. Since the text files might be hella long. Does this until peer closes connection
    while True:
        chunk = recv_socket.recv(4096)
        if not chunk: #empty connection
             break
        buffer = buffer + chunk
    
    # Checking to make sure my header is good, if it is, then check to make sure my byte length is good
    header_idx = buffer.find(b"\r\n\r\n") # Assuming there is not carriage return in the actual file
    if header_idx == -1:
        print("Error 500 Internal Server error\n") # TODO: Get correct error code
        return -1
    
    header = buffer[:header_idx].decode()

    rfc_bytes = buffer[header_idx + 4:]
    header_sections = header.split("\r\n")
    status_sections = header_sections[0].split(" ")
    if(status_sections[0] != VERSION_STR):
        print("Error 505 P2P-CI Version Not Supported\n")
    
    try:
        status_code = int(status_sections[1])
    except:
        print("Debug need int value\n") # TODO: remove this debug statemnet later with an actual debug
        return -1
    
    if status_code != 200:
        print(f"{status_code} {status_sections[2]}\n")
        return -1
    
    content_sizing_sections = header_sections[4].split(' ')

    data_amount = int(content_sizing_sections[1])
    if len(rfc_bytes) != data_amount:
        print("Error 500 Internal Server Error\n") # TODO: Give this a better statement

    # Making a directory in case this peer doesnt have one made yet
    os.makedirs("./RFC", exist_ok = True)
    rfc_path = "./RFC/rfc" + rfc_num + ".txt"

    f = open(rfc_path,"wb")
    f.write(rfc_bytes)
    print("Saved RFC Data\n")
    recv_socket.close()
    return 0

