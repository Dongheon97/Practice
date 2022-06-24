import socket
import pickle
import sys
import os
import logging
import time

class CSocket():
    def __init__(self, givenIP, givenPORT):
        self.IP = givenIP
        self.PORT = givenPORT
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def dict_to_pickle(self, givenDict):
        converted = pickle.dumps(givenDict)
        return converted

    def str_file_size(self, givenPath):
        file_size = os.path.getsize(givenPath)
        logging.info(file_size)
        return str(file_size)
    
    def send_pickle(self, givenPath):
        self.client_socket.connect((self.IP, self.PORT))
        file_size = self.str_file_size(givenPath)
        to_send = 'size' + file_size
        self.client_socket.send(to_send.encode())
        time.sleep(1)
        logging.info('File Size: {}'.format(to_send))
        
        logging.info('Sending Start')
        data_transferred = 0
        with open(givenPath, 'rb') as f:
            try:
                data = f.read(1024)
                while data:
                    print(data)
                    data_transferred = self.client_socket.send(data)
                    data = f.read(1024)
                    if data_transferred ==0:
                        break
            except Exception as e:
                logging.info(e)


if __name__=='__main__':
    logging.basicConfig(
        format='[%(levelname)s][%(asctime)s]: %(message)s', level=getattr(logging, "INFO"),
        datefmt='%H:%M:%S'
    )

    IP = '54.180.8.111'
    PORT = 80
    #IP = '127.0.0.1'
    #PORT = 8080
    PATH = './models/weights.pickle'

    csocket = CSocket(IP, PORT)
    csocket.send_pickle(PATH)

    time.sleep(100)

