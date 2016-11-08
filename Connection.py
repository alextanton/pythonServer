class Connection:
    def __init__(self, unique,ip, hostname, socket):
        self.ip = ip
        self.hostname = hostname
        self.socket = socket
        self.unique = unique