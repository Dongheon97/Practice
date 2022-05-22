#################### TO DO ####################
# dataloader 구현
# input data, test data 구현

from torch import nn, optim
import torch
from models import models
from utils.config import Config
#from utils.data import get_test_data()
from torch.utils.data import DataLoader
#import copy
import numpy as np
import logging

class Server:
    def __init__(self, config):
        self.config = config
        self.global_weights = []
        self.model = self.load_model()
        ################  TO DO  ################
        #self.testset = get_data()

    def load_model(self):
        model = models.get_model()
        return model

    def test(self, glob_weights):
        # set_weights
        self.model.load_state_dic(glob_weights)
        
        corrects = 0
        test_loss = 0
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model.to(device)
        self.model.eval()
        criterion = nn.CrossEntropyLoss()

        dataloader = DataLoader(self.testset, batch_size=32, shuffle=True)
        for batch_id, (inputs, labels) in enumerate(dataloader):
            loss = 0
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            _, preds = torch.max(outputs, 1)
            test_loss += loss.item() * inputs.size(0)
            corrects += torch.ssum(preds == labels.data)

        acc = int(corrects) / len(dataloader.dataset)
        avg_loss = test_loss / len(dataloader.dataset)
        return acc, avg_loss

'''
if __name__=="__main__":
    #config = Config("./configs/params.json")
    server = Server()
    server.run()
'''

