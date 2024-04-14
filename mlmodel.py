import numpy as np
import pandas as pd
import physics as phys
import random
from planet import Planet

random.seed(1002)
saved_states = []

def get_saved_states():
    return saved_states


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

    # Real high weigting for different number of planets: its bad
    w1 = 1E10

    # normal weight for conservation of mass
    w2 = 1
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
    # print("ee are in RNumPlanets", ans)
    return ans

def RConserved(planets: list) -> float:
    # The smaller the sum the better (conservation of energy) - Centripetal and Gravitational Forces are in Equilibrium
    # Returns a score of 1 if the sum is the best (energy all conserved), 0 if the sum is the worst (energy lost none conserved)
    sum = 0
    if len(planets) == 1:
        return 0
    if len(planets) == 0:
        return 0

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
    step_size = period // 2

    for i in range(period):
        planets = phys.updateAllObjects(planets)

        if i % step_size == 0 and i != 0:
            saved_states.append(planets)

    return planets


def populate(p: int, n: int): # p is the number of states, n is the number of planets in each state
    population = []
    for _ in range(p):
        state = [] 
        for _ in range(n):
            q = Planet()
            q.attributes.mass = random.randint(1,10)
            q.attributes.radius = random.uniform(1, 5)*0.07
            q.attributes.position = [random.randint(-10,10), random.randint(-10,10), random.randint(-10,10)]
            q.attributes.velocity = [random.randint(0,10)*5E-6, random.randint(0,10)*5E-6, random.randint(0,10)*5E-6]
            state.append(q)
        population.append(state)

    return population


def evolve(pop: list, t: int):
    # in case the parent threshold is bigger than the population size, normalise
    if t > len(pop):
        t = len(pop)

    # Make key,pair of state and r score
    scores = [(state, rewardFunc(simulate(state, 10), len(state))) for state in pop]
    # sort by score
    scores.sort(key=lambda x: x[1], reverse=True)

    # take top t performing states
    top_t = scores[:t]

    parents = [parent[0] for parent in top_t]

    seed = []
    for _ in range(t):
        rand = random.randint(0, t)
        seed.append(rand)

    diff = len(pop) - t

    children = []
    # We are making new children to make a population of the same size
    for _ in range (diff):
        # Each child should have length of the others
        random_mum = parents[random.randint(0,len(parents)-1)]
        random_dad = parents[random.randint(0, len(parents)-1)]
        child = random_mum

        for i in range(len(child)):
            if random.uniform(0,1) > 0.4:
                if i < len(random_dad):
                    child[i] = random_dad[i]

        children.append(child)

    return parents + children


def genetic(pop_size, no_planets, evolutions, harshness):
    pop = populate(pop_size, no_planets)

    for _ in range(evolutions):
        pop = evolve(pop, harshness)

    return saved_states

start = 0
pop = populate(10, 5)
for s in pop:
    start += RConserved(s)


for _ in range(5):
    pop = evolve(pop, 2)


end=0
for s in pop:
    end+= RConserved(s)
    print(RConserved(s))


print(f"Average start value: {start / 10}")
print(f"Average end value:   {end / 10}")
print(f"Percentage improvement: {(start - end)/start * 100}")
