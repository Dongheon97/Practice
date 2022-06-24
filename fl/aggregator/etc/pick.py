import pickle
import torch

with open('./dummy/0.pickle', 'rb') as inputfile:
    0_weights = pickle.load(inputfile)

with open('./dummy/1.pickle', 'rb') as inputfile:
    1_weights = pickle.load(inputfile)

with open('./dummy/2.pickle', 'rb') as inputfile:
    2_weights = pickle.load(inputfile)

b0 = 0_weights[1].values()
b1 = 1_weights[1].values()
b2 = 2_weights[1].values()

print(b0)
print(b1)
print(b2)


