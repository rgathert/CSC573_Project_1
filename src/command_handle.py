from enum_codes import HttpStatus, CommandType
from server_object import peer, rfc_idx

# TODO: See if it would be better to add here or to add in server section and break out.
# Currently, ADD requires the manager since multiple processes can append to that list
def ServerRequestParse(command_string, client_name, port_num):
    command_lines = command_string.split('\r\n')
    method_line = command_lines[0].split(' ')
    host_header = command_lines[1].split(' ')
    port_header = command_lines[2].split(' ')
    title_header = command_lines[3].split(' ')
    print(f"Method Line: {method_line}\nHost Header: {host_header}\nPort Header: {port_header}\nTitle Header: {title_header}\n")

    # Making sure the host and port header match what is expected
    if host_header[0] != "Host:" or (host_header[1]) != client_name:
        return (CommandType.INVALID, HttpStatus.BAD_REQUEST)
    if port_header[0] != "Port:" or int(port_header[1]) != port_num:
        return (CommandType.INVALID, HttpStatus.BAD_REQUEST)

    if method_line[0] == "LIST" and method_line[1] == "ALL" and method_line[2] == "P2P-CI/1.0":
        return (CommandType.LIST, HttpStatus.OK)
    
    if method_line[0] == "ADD" and method_line[1] == "RFC":
        if len(command_lines) != 4:
            return (CommandType.INVALID, HttpStatus.BAD_REQUEST, None)

        title_header = command_lines[3].split(': ', 1)
        if len(title_header) != 2 or title_header[0] != "Title":
            return (CommandType.INVALID, HttpStatus.BAD_REQUEST, None)

        rfc_num = method_line[2]
        version = method_line[3] if len(method_line) > 3 else None

        if version != "P2P-CI/1.0":
            return (CommandType.INVALID, HttpStatus.VERSION_NOT_SUPPORTED, None)

        parsed_data = {
            "rfc_num": rfc_num,
            "title": title_header[1],
        }
        return (CommandType.ADD, HttpStatus.OK, parsed_data)

    # Handling the command given
    if method_line[0] == "LIST":
        if title_header == "":
            return (CommandType.LIST, HttpStatus.OK)
        else:
            return (CommandType.LIST, HttpStatus.BAD_REQUEST)
    else:
        return (CommandType.INVALID, HttpStatus.BAD_REQUEST)
    
def List(header, rfc_list):

    message = header
    print(f"header: {header}")
    for rfc in rfc_list:
        message = f"{message}\r\n{rfc.RFC_num} {rfc.title}.txt {rfc.host_name} {rfc.port_num}"

    return message
    
    