import numpy as np
import pandas as pd
import physics as phys
import random
from planet import Planet, PlanetAttributes


def planet_to_array(planet: PlanetAttributes):
    p = []
    p.append(planet.mass)
    p.append(planet.radius)
    p.append(planet.position)
    p.append(planet.velocity)
    return p


def rewardFunc (planets: list, original_num: int) -> float:
    # Objects is a list of objects. Each object has properties: mass, radius, position, velocity
    # Position and Velocity are 3D vectors: [x,y,z]
    w1,w2 = 1,1
    reward = 0
    reward += w1 * RNumPlanets(planets, original_num)  #[0,1] - 0 is best, 1 is worst
    reward += w2 * RConserved(planets)  #[0,1] - 0 is best, 1 is worst
    #At this point reward is in the range [0,2] where 0 is best and 2 is worst

    # Normalise reward to [-1,1] so that -1 is worst and 1 is best 
    max_reward = w1 + w2
    reward = -1*(reward-1)/max_reward
    return reward

def RNumPlanets(planets: list, original_num: int) -> float:
    return (original_num-len(planets))/original_num

def RConserved(objects):
    # The smaller the sum the better (conservation of energy) - Centripetal and Gravitational Forces are in Equilibrium
    # Returns a score of 1 if the sum is the best (energy all conserved), 0 if the sum is the worst (energy lost none conserved)
    sum = 0
    for object in objects:
        for object2 in objects:
            if object == object2:
                continue
            sum += abs((phys.GRAVITATIONAL_CONSTANT * object2.mass)/np.linalg.norm(object2.position - object.position) - (object2.velocity)**2)
        if sum == 0:
            return 1
        else:
            return 1/sum

# Given the states of planets and a simulation period, p, updates the states of the system p times and returns the final state
def simulate (planets: list, period: int) -> list:
    for _ in range(period):
        planets = phys.updateAllObjects(planets)
    return planets


def populate(p: int, n: int):
    population = []
    for _ in range(p):
        state = [] 
        for _ in range(n):
            planet = PlanetAttributes
            planet.mass = random.randint(1,10)
            planet.radius = random.uniform(1, 10)
            planet.position = [random.randint(0,10), random.randint(0,10), random.randint(0,10)]
            planet.velocity = [random.randint(0,10), random.randint(0,10), random.randint(0,10)]
            state.append(planet)
        population.append(state)

    return population

