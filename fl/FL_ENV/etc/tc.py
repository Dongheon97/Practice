import socket
from client import Client
from utils.config import Config
import sys
import pickle
import time
import torch

HOST = '54.180.8.111'
PORT = 80

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

print('connected')
'''
config = Config('./configs/params.json')
client = Client(config)
weights = client.load_weights('./models/full.pth')
'''

#model = torch.load('./models/full.pth')
#weights = model.state_dict()

#print(weights)

with open('./weights.pickle', 'rb') as f:
    weights = pickle.load(f)
print(weights.keys())

dict2pickle = pickle.dumps(weights)

got_byte = sys.getsizeof(dict2pickle)
to_send = 'size' + str(got_byte)
print(got_byte)
print(to_send)

client_socket.send(to_send.encode())

print('send \'to_send\'')
time.sleep(1)
'''
# Save Json file
with open('./weights.pickle', 'wb') as outputfile:
    orderedDict to Json
    pickle.dump(weights, outputfile)

with open('./weights.pickle', 'rb') as inputfile:
   weights = pickle.load(inputfile) 
'''
client_socket.sendall(dict2pickle)

client_socket.close()

