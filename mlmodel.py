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

