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
    def __init__(self, given_xml_file, given_num_frames, given_batch_size):
        self.sim = MjSim(given_xml_file)
        self.num_frames = given_num_frames
        self.batch_size = given_batch_size
        self.losses = []

    def reorder_state(self, qpos, qvel):
        # qpos: [cart_position, pole_angle]
        # qvel: [cart_velocity, pole_angular_velocity]
        # -> [cart_position, cart_velocity, pole_angle, pole_angular_velocity]
        reordered = list(it.chain(*zip(qpos, qvel)))
        return reordered

    def is_fall(self, curr_state):
        # -pi/15 <= pole_angle(rad) <= pi/15
        if(curr_state[2] >= -0.20944 and curr_state[2] <= 0.20944):
            return False
        else:
            return True

    def mj_step(self, givenAction):
        # set_action -> step -> next_state, reward, done 
        self.sim.data.ctrl[:] = givenAction
        self.sim.step()
        
        obv = self.sim.get_state()
        next_state = self.reorder_state(obv[1], obv[2])
        
        done = self.is_fall(next_state)
        reward = 1
        return next_state, reward, done

    def main(self):
        viewer = MjViewer(self.sim)
        init_state = self.sim.get_state()
        sim_state = self.reorder_state(init_state[1], init_state[2])

        while True:
            episode_reward = 0
            self.sim.set_state(init_state)
            for i in range(self.num_frames):
                if((i%2) == 0):
                    action = 0.5
                else:
                    action = -0.5
                next_state, reward, done = self.mj_step(action)
                episode_reward += reward
                print(f'next_state: {next_state}')
                print(f'Episode_reward: {episode_reward}, Frame_reward: {reward}')
                print(f'done: {done}')
                viewer.render()
            if os.getenv('TESTING') is not None:
                break

if __name__=="__main__":
    PATH = '/home/dnclab/dev/mi333/simulator/xmls/cartpole.xml'
    num_frames = 1000
    batch_size = 32
    gamma = 0.99
    xml_file = load_model_from_path(PATH)
    cartpole = MjCartPole(xml_file, num_frames, batch_size)
    cartpole.main()
