import numpy as np
import random
from matplotlib import pyplot as plt

population_size = 300
Prc = 0.1
Prm = 0.001
iterations = 1000

class Cities:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def generate_distance(self, city):
        xd = abs(self.x - city.x)
        yd = abs(self.y - city.y)
        d = np.sqrt((xd ** 2) + (yd ** 2))
        return d

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"


def generate_route(cities):
    route = random.sample(cities, len(cities))
    return route


def population(pop_size, cities):
    population = []

    for i in range(0, pop_size):
        population.append(generate_route(cities))
    return population


def fitness_calc(route):
    distance = 0
    for i in range(0, len(route)):
        city_a = route[i]
        if i + 1 < len(route):
            city_b = route[i + 1]
        else:
            city_b = route[i - 1]
        distance += city_a.generate_distance(city_b)
    fitness = 1 / float(distance)
    return fitness


def elitist_selection(fitness, routes, r=4):
    n = len(fitness)
    temp = np.array(fitness)
    max_ids = (-temp).argsort()[:n]

    new_routes = []
    a = population_size - r
    for l in range(0, a):
        new_routes.append(generate_route(cities))
    i = 0
    while len(new_routes) < population_size:

        ind = routes[max_ids[i]]
        if i != 0:

            if random.uniform(0, 1) < Prc:
                a = random.randint(0, len(routes) - 1)

                ind = crossover(ind, routes[max_ids[a]])

            if random.uniform(0, 1) < Prm:
                ind = mutation(ind)
        i = i + 1

        new_routes.append(ind)
    return new_routes

def crossover(ind1, ind2):
    point = random.randint(0, len(ind1) - 1)
    child = ind1.copy()
    child.remove(ind2[point])
    child.insert(point, ind2[point])
    return child


def mutation(ind):
    point = random.randint(0, len(ind) - 2)
    test = ind.copy()
    tempind = test[point]
    test[point] = test[point + 1]
    test[point + 1] = tempind
    return test


if __name__ == '__main__':
    cities = []
    random.seed(0)
    for i in range(0, 10):
        cities.append(Cities(x=int(random.random() * 200), y=int(random.random() * 200)))
    routes = []
    fitness = []
    for i in range(0, population_size):
        routes.append(generate_route(cities))
        fitness.append(fitness_calc(routes[i]))
    i = 0
    a=0
    index=0
    while i < iterations:
        routes = elitist_selection(fitness, routes, r=4)
        fitness = []
        for k in range(0, len(routes)):
            fitness.append(fitness_calc(routes[k]))
        if i % 100 == 0:
            print("Gen " + str(i) + ": " + str(max(fitness)))
        i = i + 1