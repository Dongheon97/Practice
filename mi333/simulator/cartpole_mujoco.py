#!/usr/bin/env python3
"""
Shows how to toss a capsule to a container.
"""
from mujoco_py import load_model_from_path, MjSim, MjViewer
import os
import torch
import torch.nn as nn
from random import *

class MjCartPole():
    def __init__(self, given_xml_file):
        self.sim = MjSim(given_xml_file)

    def is_fall(self, givenAngle):
        # -pi/15 <= pole_angle(rad) <= pi/15
        if(givenAngle <= -0.2094 and givenAngle >= 0.2094):
            return False
        else:
            return True

    def is_done(self, givenReward):
        if(givenReward >= 200):
            return 

    def mj_step(self, givenAction):
        

xml_file = load_model_from_path("./xmls/cartpole.xml")
sim = MjSim(xml_file)

viewer = MjViewer(sim)

sim_state = sim.get_state()

#sim.set_state(sim_state)

while True:
    #print(sim_state)
    sim.set_state(sim_state)

    for i in range(200):
        
        if i<100:
            sim.data.ctrl[:] = 0.1
            #sim.data.ctrl[0:] = -1.0
            #sim.data.ctrl[1:] = 0.0
        else:
            sim.data.ctrl[:] = 0.1
            #sim.data.ctrl[0:] = 0.0
            #sim.data.ctrl[1:] = -1.0
        sim.step()
        #print(sim.get_state())
        viewer.render()

    if os.getenv('TESTING') is not None:
        break

if __name__=="__main__":
    PATH = '/home/dnclab/dev/mi333/simulator/xmls/cartpole.xml'
    xml_file = load_model_from_path(PATH)
    cartpole = MjCartPole(xml_file)
    
