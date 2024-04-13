import numpy as np
import tensorflow as tf
import pandas as pd
import physics as phys

def rewardFunc (planets: list, original_num: int) -> float:
    # Objects is a list of objects. Each object has properties: mass, radius, position, velocity
    # Position and Velocity are 3D vectors: [x,y,z]
    w1,w2 = 1,1
    reward = 0
    reward += w1 * RNumPlanets(planets, original_num)  #[0,1]
    reward += w2 * RConserved(planets)  # Reward for conserving energy
    # NORMALISE REWARD HERE
    reward = reward #HEREEEEEEEEEE
    return reward

def RNumPlanets(planets: list, original_num: int) -> float:
    return (original_num-len(planets))/original_num

def RConserved(objects):
    sum = 0
    for object in objects:
        for object2 in objects:
            if object == object2:
                continue
            sum += abs((phys.GRAVITATIONAL_CONSTANT * object2.mass)/np.linalg.norm(object2.position - object.position) - (object2.velocity)**2)
    return sum

