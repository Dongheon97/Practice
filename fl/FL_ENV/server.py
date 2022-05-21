import torch
import models import models
import utils.config import Config
import copy
import numpy as np
import logging

class Server:
    def __init__(self):
        #self.config = config
        self.model = self.load_model()

    def run(self):


    def load_model(self):
        model = models.get_model()
        logging.debug(model)
        return model

if __name__=="__main__":
    #config = Config("./configs/params.json")
    server = Server()
    server.run()
