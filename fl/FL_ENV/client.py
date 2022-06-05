from torch import nn, optim
import torch
#import copy
from models import models
from utils.config import Config
from utils.data import get_data
from torch.utils.data import DataLoader
import logging
import sys

import socket

class Client:
    def __init__(self, config):
        self.config = config
        self.model = self.load_model()
        self.train_loader = None
        self.test_loader = None
        self.local_weights = None

    def load_model(self):
        logging.info("Load_model: {}".format(self.config.dataset))
        model = models.get_model()
        return model

    def load_train_data(self):
        trainset, testset = get_data(self.config.dataset, self.config)
        self.train_loader = DataLoader(trainset, batch_size=self.config.fl.batch_size)
        self.test_loader = DataLoader(testset, batch_size=self.config.fl.batch_size)

    def train(self, path, verbose=1):
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        
        # set weights 
        #self.model.load_state_dict(glob_weights)dd

        self.model.to(device)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(params=self.model.parameters(), lr=self.config.fl.lr)

        logging.info("Start training")
        for e in range(self.config.fl.epochs):
            running_loss = 0
            running_corrects = 0
            epoch_loss = 0
            epoch_acc = 0

            for inputs, labels in self.train_loader:
                inputs = inputs.to(device)
                labels = labels.to(device)
                optimizer.zero_grad()
                outputs = self.model(inputs)
                loss = criterion(outputs, labels)
                _, preds = torch.max(outputs, 1)
                loss.backward()
                optimizer.step()
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)
            
            epoch_loss = running_loss / len(self.train_loader.dataset)
            epoch_acc = int(running_corrects) / len(self.train_loader.dataset)

            
            for name, param in self.model.named_parameters():
                logging.info("name: {}".format(name))
                logging.info(param[0].type())
                #logging.info(param)
                logging.info("param.shape: {}".format(param.shape))
                #logging.info("param.requires_grad: {}".format(param.requires_grad))
                logging.info("=====")
            

            test_model = self.model
            test_acc, _ = self.test(test_model)

            self.local_weights = self.model.state_dict()
            logging.info("Weights Size: {}".format(sys.getsizeof(self.local_weights)))

            logging.info("Epochs: {}, Loss: {:.4f}, Train_Acc: {:.4f}, Test_Acc: {:.4f}".format(e+1, epoch_loss, epoch_acc, test_acc))
        #info = {"weights": self.local_weights, "loss": epoch_loss, 
                "corrects": running_corrects, "len": len(self.train_loader.dataset)}
        '''
        # Save only weights
        torch.save(self.local_weights, path+"weights_only.pth")
        # Save full model
        torch.save(self.model, path+"full.pth")
        '''
        return info

    def test(self, model):
        corrects = 0
        test_loss = 0
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        #model = copy.deepcopy(self.model)
        model.to(device)
        model.eval()
        criterion = nn.CrossEntropyLoss()

        #dataloader = DataLoader(self.testset, batch_size=32, shuffle=True)
        for inputs, labels in self.test_loader:
            loss = 0
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            _, preds = torch.max(outputs, 1)
            test_loss += loss.item() * inputs.size(0)
            corrects += torch.sum(preds == labels.data)

        acc = int(corrects) / len(self.test_loader.dataset)
        avg_loss = test_loss / len(self.test_loader.dataset)
        # print(corrects)
        # print(len(dataloader.dataset))
        # print(f"test_acc:{acc}",)
        return acc, avg_loss

    def load_weights(self, givenPath):
        model_load = torch.load(givenPath)
        '''
        for name, param in model_load.named_parameters():
                logging.info("name: {}".format(name))
                logging.info("name tpye: {}".format(type(name)))
                logging.info(param[0].type())
                logging.info(type(param))
                logging.info("param.shape: {}".format(param.shape))
                #logging.info("param.requires_grad: {}".format(param.requires_grad))
                logging.info("=====")
        '''
        weights = model_load.state_dict()
        logging.info("dict length: {}".format(len(weights)))
        logging.info(weights.keys())
        logging.info(weights.values())
        return weights

        #weights = model_load.load_state_dict(givenPath)
        #for name, param in model_load.named_parameters():
        #    logging.info('param.shape: {}'.format(param.shape))


if __name__ == "__main__":
    logging.basicConfig(
        format='[%(levelname)s][%(asctime)s]: %(message)s', level=getattr(logging, "INFO"),
        datefmt='%H:%M:%S'
    )

    ip = '54.180.8.111'
    port = 80
    model_path = './models/'
    
    config = Config('./configs/params.json')
    client = Client(config)
    client.load_train_data()
    #info = client.train(model_path)

    client.load_weights(model_path+"full.pth")

