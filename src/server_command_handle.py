from enum_codes import HttpStatus, CommandType
from server_object import peer, rfc_idx

# TODO: See if it would be better to add here or to add in server section and break out.
# Currently, ADD requires the manager since multiple processes can append to that list

# Following function parses the command being requested to make sure its not a bad request
# If it is a valid request, it returns the request type, along with an HTTPStatus of OK
# This will be used for error handling later down the line.
def ServerRequestParse(command_string, client_name, port_num):
    command_lines = command_string.split('\r\n')
    
    # Returning if there is not any valit type
    if len(command_lines) < 3:
        return (CommandType.INVALID, HttpStatus.BAD_REQUEST, None)
    method_line = command_lines[0].split(' ')
    host_header = command_lines[1].split(' ')
    port_header = command_lines[2].split(' ')

    # TODO: Remove debugging line before submitting
    print(f"Method Line: {method_line}\nHost Header: {host_header}\nPort Header: {port_header}\n")

    # Making sure the host and port header match what is expected, additionally, makes
    # sure our version number is ok.
    if host_header[0] != "Host:" or host_header[1] != client_name:
        return (CommandType.INVALID, HttpStatus.BAD_REQUEST, None)
    if port_header[0] != "Port:" or int(port_header[1]) != port_num:
        return (CommandType.INVALID, HttpStatus.BAD_REQUEST, None)
    
    
    # Simple List Request 
    # TODO: Add in handling for if the list array is too long (extra data added)
    if len(method_line) == 3 and method_line[0] == "LIST" and method_line[1] == "ALL":
        if method_line[2] != "P2P-CI/1.0":
            return (CommandType.LIST, HttpStatus.VERSION_NOT_SUPPORTED, None)
        
        parsed_data = {
            "host": host_header[1],
            "port": int(port_header[1]),
        }
        return (CommandType.LIST, HttpStatus.OK, parsed_data)
    

    if len(method_line) == 4 and method_line[0] == "ADD" and method_line[1] == "RFC":

        if method_line[3] != "P2P-CI/1.0":
            return (CommandType.ADD, HttpStatus.VERSION_NOT_SUPPORTED, None)
    
        if len(command_lines) < 4:
            return (CommandType.INVALID, HttpStatus.BAD_REQUEST, None)

        title_header = command_lines[3].split(': ', 1)
        if title_header[0] != "Title":
            return (CommandType.INVALID, HttpStatus.BAD_REQUEST, None)

        title = title_header[1]        
        rfc_num = method_line[2]
    
        parsed_data = {
            "rfc_num": rfc_num,
            "title": title_header[1],
            "host": host_header[1],
            "port": int(port_header[1]),
        }
        return (CommandType.ADD, HttpStatus.OK, parsed_data)
    
    if len(method_line) == 4 and method_line[0] == "LOOKUP" and method_line[1] == "RFC":
        if method_line[3] != "P2P-CI/1.0":
            return (CommandType.LOOKUP, HttpStatus.VERSION_NOT_SUPPORTED, None)

        try:
            rfc_num = int(method_line[2])
        except ValueError:
            return (CommandType.INVALID, HttpStatus.BAD_REQUEST, None)

        title = ""
        if len(command_lines) >= 4:
            title_header = command_lines[3].split(': ', 1)
            if title_header[0] == "Title":
                title = title_header[1]

        parsed_data = {
            "rfc_num": rfc_num,
            "title": title,
            "host": host_header[1],
            "port": int(port_header[1]),
        }
        return (CommandType.LOOKUP, HttpStatus.OK, parsed_data)

    return (CommandType.INVALID, HttpStatus.BAD_REQUEST, None)

def Lookup(header, rfc_num, rfc_list):
    matches = [rfc for rfc in rfc_list if int(rfc.RFC_num) == int(rfc_num)]
    if not matches:
        return None

    response = header + "\r\n"
    for rfc in matches:
        response += f"RFC {rfc.RFC_num} {rfc.title} {rfc.host_name} {rfc.port_num}\r\n"
    response += "\r\n"
    return response
 
def List(header, rfc_list):

    message = header + "\r\n"
    # print(f"header: {header}")
    for rfc in rfc_list:
        message += f"RFC {rfc.RFC_num} {rfc.title} {rfc.host_name} {rfc.port_num}\r\n"
    message += "\r\n"
    return message

def Add(header, rfc_num, title, peer_obj, rfc_list):
    for rfc in rfc_list:
        if (int(rfc.RFC_num) == int(rfc_num) and
            rfc.host_name == peer_obj.host_name and
            int(rfc.port_num) == int(peer_obj.port_num)):
            return header + "\r\n" + f"RFC {rfc_num} {title} {peer_obj.host_name} {peer_obj.port_num}\r\n\r\n"

    rfc_list.append(rfc_idx(title, rfc_num, peer_obj))
    return header + "\r\n" + f"RFC {rfc_num} {title} {peer_obj.host_name} {peer_obj.port_num}\r\n\r\n"
    