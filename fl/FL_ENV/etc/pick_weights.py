import pickle
import torch

with open('./weights.pickle', 'rb') as inputfile:
    weights = pickle.load(inputfile)

print(weights)

