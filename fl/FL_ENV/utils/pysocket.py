import socket

class Socket():
    def __init__(self, givenIP, givenPORT):
        self.ip = givenIP
        self.port = givenPORT
    
    def socket_send(self, cmd, givenSocket):
        data = pickle.dumps(cmd)
        client.sendall(data)
        return 0


