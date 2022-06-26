#!/usr/bin/env python3
"""
Shows how to toss a capsule to a container.
"""
from mujoco_py import load_model_from_path, MjSim, MjViewer
import os
import torch
import torch.nn as nn
from random import *
import itertools as it

class MjCartPole():
    def __init__(self, given_xml_file, ):
        self.sim = MjSim(given_xml_file)

    def reorder_state(self, qpos, qvel):
        # qpos: [cart_position, pole_angle]
        # qvel: [cart_velocity, pole_angular_velocity]
        # -> [cart_position, cart_velocity, pole_angle, pole_angular_velocity]
        reordered = list(it.chain(*zip(qpos, qvel)))
        return reordered

    def is_fall(self, curr_state):
        # -pi/15 <= pole_angle(rad) <= pi/15
        if(curr_state[2] <= -0.20944 and curr_state[2] >= 0.20944):
            return False
        else:
            return True

    def mj_step(self, givenAction):
        # set_action -> step -> next_state, done, _ 
        self.sim.data.ctrl[:] = givenAction
        self.sim.step()
        
        obv = self.sim.get_state()
        next_state = self.reordered_state(obv[1], obv[2])
        
        done = self.is_fall(next_state)
        return next_state, done

    def main(self):
        viewer = MjViewer(self.sim)
        init_state = self.sim.get_state()
        sim_state = self.reorder_state(init_state[1], init_state[2])
        while 
'''
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
        else:
            sim.data.ctrl[:] = 0.1
        sim.step()
        #print(sim.get_state())
        viewer.render()

    if os.getenv('TESTING') is not None:
        break
'''
if __name__=="__main__":
    PATH = '/home/dnclab/dev/mi333/simulator/xmls/cartpole.xml'
    xml_file = load_model_from_path(PATH)
    cartpole = MjCartPole(xml_file)
    
