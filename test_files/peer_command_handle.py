from enum_codes import HttpStatus, CommandType, returnPhrase
import datetime
import platform
import os
## Functions for handling peer to peer and peer to server communication requests
#TODO: Find way to abstract this
VERSION_STR = "P2P-CI/1.0"

# Parsing a Get Request
def PeerRequestParse(request, host_name):
    
    request_lines = request.split('\r\n')
    if len(request_lines) < 3: # Check this to make sure we dont get an error at this index
        return(CommandType.INVALID, HttpStatus.BAD_REQUEST, None)
    method_line = request_lines[0].split(' ')
    host_header = request_lines[1].split(' ')
    os_header   = request_lines[2].split(' ',1)

    # TODO: Remove debugging line before submASitting
    print(f"Method_line: {method_line}\nHost_header: {host_header}\nOS_Header: {os_header}\n")

    # Making sure the host header match what is expected
    if host_header[0] != "Host:" or host_header[1] != host_name:
        return (CommandType.INVALID, HttpStatus.BAD_REQUEST, None)
    
    if os_header[0] != "OS:" or len(os_header) < 2:
        return (CommandType.INVALID, HttpStatus.BAD_REQUEST, None)
    
    rfc = method_line[2]
    
    # Checking to see if we can actually convert to an RFC
    try:
        rfc_val = int(rfc)
    except ValueError:
        return (CommandType.INVALID, HttpStatus.BAD_REQUEST, None)
    
    # Parsed Message
    parsed_request = {
        "rfc_val":  rfc_val,
        "host":     host_name,
    }

    return (CommandType.GET, HttpStatus.OK, parsed_request)


# Generating the transmission for a file being sent over
def fileSend(header, file_path):
    
    # Date parsing
    date_str = datetime.datetime.now(datetime.timezone.utc).strftime('%A, %d %b %Y %H:%M:%S GMT')
    date_msg = "Date: " + date_str + "\r\n"

    # OS Parsing
    os_type = platform.system()
    os_version = platform.release()
    os_msg = "OS: " + os_type + " " + os_version + "\r\n"

    # File mod parsing
    file_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path), tz=datetime.timezone.utc)
    file_time_formatted = file_time.strftime('%A, %d %b %Y %H:%M:%S GMT')
    file_msg = 'Last-Modified: ' + file_time_formatted + '\r\n'

    # File parsin
    f = open(file_path,'rb')
    data = f.read()
    f.close()

    content_len_msg = "Content-Length: " + str(len(data)) + "\r\n"
    content_type_msg = "Content-Type: text/plain \r\n"

    # Constructing the message
    msg = header + date_msg + os_msg + file_msg + content_len_msg + content_type_msg + "\r\n" + data.decode()

    return msg


# TODO: Build the GET, LIST, LOOKUP, and ADD requests as seperate functions below

def getRequest(rfc_num, target_host):
    
    msg = (f"GET RFC {rfc_num} {VERSION_STR}\r\n"
           f"Host: {target_host}\r\n"
           f"OS: {platform.system()} {platform.release()}\r\n\r\n")
    
    return msg

def addRequest(rfc_num, host_name, p2p_port, client_socket, rfc_paths):

    file_path = f"./RFC/rfc{rfc_num}.txt"
    if not os.path.exists(file_path):
        print(f"Unable to find file\n")
        return

    msg = (f"ADD RFC {rfc_num} P2P-CI/1.0\r\n"
            f"Host: {host_name}\r\n"
            f"Port: {p2p_port}\r\n"
            f"Title: {rfc_num}.txt\r\n\r\n")
    
    client_socket.send(msg.encode())
    data = client_socket.recv(65535)

    return_message = data.decode()
    header_lines = return_message.split("\r\n")
    status_sections = header_lines[0].split(" ")

    if int(status_sections[1]) == HttpStatus.OK.value:
        rfc_paths[int(rfc_num)] = file_path



    #TODO: Remove this debug message later on.
    print(return_message)



    return

def listRequest(host_name, p2p_port, client_socket):
    msg = f"LIST ALL P2P-CI/1.0\r\nHost: {host_name}\r\nPort: {p2p_port}\r\n\r\n"
    client_socket.send(msg.encode())

    # TODO: Remove this later
    data = client_socket.recv(65535)
    print(data.decode())
