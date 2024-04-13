import numpy as np
import tensorflow as tf
import pandas as pd
import physics as phys

NUMBEROFPLANETS = ...

def rewardFunc (planets: list, original_num: int) -> int :
    # Objects is a list of objects. Each object has properties: mass, radius, position, velocity
    # Position and Velocity are 3D vectors: [x,y,z]
    w1,w2 = 1,1
    reward = 0

    reward += w1 * RNumPlanets(planets)  #[0,1]
    reward += w2 * RConserved(planets)  # Reward for conserving energy

    # NORMALISE REWARD HERE
    reward = reward #HEREEEEEEEEEE

    return reward

def RNumPlanets(planets: list) -> int:
    return (NUMBEROFPLANETS-len(planets))/NUMBEROFPLANETS

def RConserved(objects):
    for object in objects:
        for object2 in objects:
            if object == object2:
                continue
            if not phys.calcGravitationalForce(object.mass, object2.mass, object.radius, object2.radius, object.position, object2.position) == 0:
                return 0
