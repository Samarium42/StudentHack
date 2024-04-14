import numpy as np
import pandas as pd
import physics as phys
import random
from planet import Planet


def planet_to_array(planet: Planet):
    p = []
    p.append(planet.attributes.mass)
    p.append(planet.attributes.radius)
    p.append(planet.attributes.position)
    p.append(planet.attributes.velocity)
    return p


def rewardFunc(planets: list, original_num: int) -> float:
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
    ans = (original_num-len(planets))/original_num
    print("We are in RNumPlanets", ans)
    return ans

def RConserved(planets: list) -> float:
    # The smaller the sum the better (conservation of energy) - Centripetal and Gravitational Forces are in Equilibrium
    # Returns a score of 1 if the sum is the best (energy all conserved), 0 if the sum is the worst (energy lost none conserved)
    sum = 0
    for p in planets:
        for q in planets:
            if p == q:
                continue
            sum += abs((phys.GRAVITATIONAL_CONSTANT * q.attributes.mass)/np.linalg.norm(np.asarray(q.attributes.position) - np.asarray(p.attributes.position) - np.asarray(q.attributes.velocity)**2))
        if sum == 0:
            return 1
        else:
            return 1/sum

# Given the states of planets and a simulation period, p, updates the states of the system p times and returns the final state
def simulate (planets: list, period: int) -> list:
    for _ in range(period):
        planets = phys.updateAllObjects(planets)
    return planets


def populate(p: int, n: int): # p is the number of states, n is the number of planets in each state
    population = []
    for _ in range(p):
        state = [] 
        for _ in range(n):
            q = Planet()
            q.attributes.mass = random.randint(1,10)
            q.attributes.radius = random.uniform(1, 10)
            q.attributes.position = [random.randint(0,10), random.randint(0,10), random.randint(0,10)]
            q.attributes.velocity = [random.randint(0,10), random.randint(0,10), random.randint(0,10)]
            state.append(q)
        population.append(state)

    return population

pop = populate(5,5)

for i in pop:
    print("Solar system:")
    for p in i:
        print(planet_to_array(p))
    print(RConserved(i))
    print("\n\n\n")


