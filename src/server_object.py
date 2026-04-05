# Creating a peer object (has hostname, and port value)
class peer:
    def __init__(self, host_name, port_num):
        self.host_name = host_name
        self.port_num = port_num

class rfc_idx:
    def __init__(self, title: str, rfc_num: int, peer_obj: peer):
        self.title = title
        self.RFC_num = rfc_num
        self.host_name = peer_obj.host_name
        self.port_num = peer_obj.port_num