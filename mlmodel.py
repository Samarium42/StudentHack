import numpy as np
import tensorflow as tf
import pandas as pd

def rewardFunc (object):
    # Objects is a list of objects. Each object has properties: mass, radius, position, velocity
    # Position and Velocity are 3D vectors: [x,y,z]
    w1,w2,w3,w4 = 0,0,0,1
    reward = 0
    reward += w1 * RBounded(object)  # Reward for staying within the bounds of the environment
    reward += w2 * REscapeTraj(object)  # Reward for not having the trajectory escape the environment MIGHT LEAVE OUT
    reward += w3 * RCollision(object)
    reward += w4 * REnergy(object)  # Reward for conserving energy
    return reward

def RBounded(obect):
    return 0

def REscapeTraj(object):
    return 0

def RCollision(object):
    return 0

def REnergy(object):
    return 0
