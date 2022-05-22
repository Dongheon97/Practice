from torch import nn, optim
import torch
#import copy
from models import models
from utils.data import get_train_data
from torch.utils.data import DataLoader

class Client:
    def __init__(self, config):
        self.config = config
        self.model = self.load_model()
        self.weights = []
        self.epoch_loss = []
        self.running_corrects = []
        self.len_dataset= []
        
        
        # self.train_data = get_train_data()


    ######### To Do ###########
    def receive_info(self):
        return

    def send_info(self):
        return

    def connect_server(self):
        return
    ###########################

    def load_model(self):
        model = models.get_model()
        return model

    def train(self, verbose=1):
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        
        # set weights 
        self.model.load_state_dic(glob_weights)
