from torch import nn, optim
import torch
from models import models
from utils.config import Config
from utils.data import get_data
from torch.utils.data import DataLoader
#import copy
import numpy as np
import logging
import pickle

class Updater:
    def __init__(self, config):
        self.config = config
        self.global_weights = []
        self.model = self.load_model()
        self.test_loader = self.load_test_data()
        self.global_weights = None

    def load_model(self):
        logging.info('Load Model: {}'.format(self.config.dataset))
        model = models.get_model()
        return model

    def load_test_data(self):
        _, testset = get_data(self.config.dataset, self.config)
        test_loader = DataLoader(testset, batch_size=32, shuffle=True)
        return test_loader

    def test(self):
        # set_weights
        self.model.load_state_dict(self.global_weights)
        
        corrects = 0
        test_loss = 0
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model.to(device)
        self.model.eval()
        criterion = nn.CrossEntropyLoss()

        #dataloader = DataLoader(self.testset, batch_size=32, shuffle=True)
        for inputs, labels in self.test_loader:
            loss = 0
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs = self.model(inputs)
            loss = criterion(outputs, labels)
            _, preds = torch.max(outputs, 1)
            test_loss += loss.item() * inputs.size(0)
            corrects += torch.sum(preds == labels.data)

        acc = int(corrects) / len(self.test_loader.dataset)
        avg_loss = test_loss / len(self.test_loader.dataset)

        logging.info("Test Accuracy: {}, Avgerage Loss: {}".format(acc, avg_loss))

        return acc, avg_loss

    def pickle_to_weights(self, filePath):
        with open(filePath, 'rb') as inputfile:
            weights = pickle.load(inputfile)
        logging.info(weights.keys())
        self.global_weights = weights


if __name__=="__main__":
    logging.basicConfig(
        format='[%(levelname)s][%(asctime)s]: %(message)s',
        level=getattr(logging, "INFO"), datefmt='%H:%M:%S'
    )
    PATH = './models/2.pickle'
    config = Config("./configs/params.json")
    updater = Updater(config)
    updater.pickle_to_weights(PATH)
    updater.test()

