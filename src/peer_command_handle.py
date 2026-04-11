from enum_codes import HttpStatus, CommandType
import datetime


# Parsing a Get Request
def PeerRequestParse(request):
    request_lines = request.split('\r\n')
    if len(request_lines) != 3: # Check this to make sure we dont get an error at this index
        return(CommandType.INVALID, HttpStatus.BAD_REQUEST, None)
    