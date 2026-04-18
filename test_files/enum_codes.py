from enum import Enum

class HttpStatus(Enum):
    OK = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404
    VERSION_NOT_SUPPORTED = 505
    SERVICE_UNAVAILABLE = 503


class CommandType(Enum):
    ADD = 1
    LOOKUP = 2
    LIST = 3
    GET = 4
    INVALID = 5


def returnPhrase(status):
    if status == HttpStatus.OK:
        return "OK"
    elif status == HttpStatus.BAD_REQUEST:
        return "Bad Request"
    elif status == HttpStatus.NOT_FOUND:
        return "Not Found"
    elif status == HttpStatus.VERSION_NOT_SUPPORTED:
        return "P2P-CI Version Not Supported"
    elif status == HttpStatus.SERVICE_UNAVAILABLE:
        return "Service Unavailable"
    else:
        return "Error"