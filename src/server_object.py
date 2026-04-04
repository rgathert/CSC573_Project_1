# Creating a peer object (has hostname, and port value)
class peer:
    def __init__(self, host_name, port_num):
        self.host_name = host_name
        self.port_num = port_num

class rfc_idx:
    def __init__(self, title, peer_type):
        self.title = title
        self.peer = peer_type