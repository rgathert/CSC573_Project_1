from enum_codes import HttpStatus, CommandType
from server_object import peer, rfc_idx

# TODO: See if it would be better to add here or to add in server section and break out.
# Currently, ADD requires the manager since multiple processes can append to that list
def ServerRequestParse(command_string, client_name, port_num):
    command_lines = command_string.split('\r\n')
    method_line = command_lines[1].split(' ')
    host_header = command_lines[2].split(' ')
    port_header = command_lines[3].split(' ')
    title_header = command_lines[4].split(' ')

    # Making sure the host and port header match what is expected
    if host_header[1] != "Host:" or int(host_header[2]) != client_name:
        return (CommandType.INVALID, HttpStatus.BAD_REQUEST)
    if port_header[1] != "Port:" or int(port_header[2]) != port_num:
        return (CommandType.INVALID, HttpStatus.BAD_REQUEST)
    
    # Handling the command given
    if method_line[1] == "LIST":
        if title_header == "":
            return (CommandType.LIST, HttpStatus.OK)
        else:
            return (CommandType.LIST, HttpStatus.BAD_REQUEST)
    else:
        return (CommandType.INVALID, HttpStatus.BAD_REQUEST)
    
def List(message, rfc_list):

    for rfc in rfc_list:
        message = f"{message}\r\n{rfc.title} {rfc.title}.txt {rfc.peer.host_name} {rfc.peer.port_num}\r\n"

    return message
    
    