import socket
from client import Client
from utils.config import Config
import sys
import pickle
import time
import torch
import os

#HOST = '54.180.8.111'
#PORT = 80

HOST = '127.0.0.1'
PORT = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

print('connected')
#model = torch.load('./models/full.pth')
#weights = model.state_dict()

#print(weights)
'''
with open('./weights.pickle', 'rb') as f:
    weights = pickle.load(f)
print(weights.keys())

dict2pickle = pickle.dumps(weights)

got_byte = sys.getsizeof(dict2pickle)
to_send = 'size' + str(got_byte)
print(got_byte)
print(to_send)

client_socket.send(to_send.encode())
'''

got_size = os.path.getsize('./weights.pickle')
to_send = 'size'+str(got_size)
client_socket.send(to_send.encode())
print('send', to_send)
time.sleep(1)

data_transferred = 0
print('sending start')
with open('./weights.pickle', 'rb') as f:
    try:
        data = f.read(1024)
        while data:
            data_transferred = client_socket.send(data)
            data = f.read(1024)
            if data_transferred ==0:
                break
    except Exception as e:
        print(e)

#client_socket.sendall(dict2pickle)

client_socket.close()

