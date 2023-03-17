import numpy as np
import matplotlib.pyplot as plt
import random


def generate_population(population_size, weights, weight_limit):
    population = []
    for i in range(0, population_size):
        individual = np.random.binomial(1, 0.5, len(weights))
        while weight_from_individual(individual, weights) > weight_limit:
            individual = np.random.binomial(1, 0.5, len(weights))
        population.append(individual)
    return population


def value_from_individual(individual, values):
    return sum(individual * values)


def weight_from_individual(individual, weights):
    return sum(individual * weights)


def fitness(population, values, weights, weight_limit):
    score = []
    for individual in population:
        value = value_from_individual(individual, values)
        weight = weight_from_individual(individual, weights)
        if weight > weight_limit:
            score.append(0)
            continue
        else:
            score.append(value)
            continue
    return score


def elitist_selection(population, values, weights, weight_limit, r):
    fitness_scores = fitness(population, values, weights, weight_limit)
    ids = list(range(0,len(population)))
    sorted_ids = [ids for fitness_scores, ids in sorted(zip(fitness_scores, ids))]
    sorted_population = []
    for id in sorted_ids:
        sorted_population.append(population[id])
    return sorted_population[-r:]


def crossover(population, Prc, population_size):
    random.shuffle(population)
    for pair in range(0, population_size, 2):
        if random.random() < Prc:
            ind1 = population[pair]
            ind2 = population[pair + 1]
            child1 = []
            child2 = []
            midpoint = random.randint(0, len(ind1) - 1)
            child1.extend(ind1[:midpoint])
            child1.extend(ind2[midpoint:])
            child2.extend(ind1[:midpoint])
            child2.extend(ind2[midpoint:])
            population[pair] = child1
            population[pair + 1] = child2
    return population


def mutation(population, Prm):
    for individual in range(0, len(population)):
        for bit in range(0, len(population[individual])):
            if random.random() < Prm:
                population[individual][bit] = 1 - population[individual][bit]
    return population


def iteration(population, values, weights, weight_limit, population_size, Prm, Prc):
    selection_p = elitist_selection(population, values, weights, weight_limit, round(0.1 * population_size))
    population_new = selection_p
    while len(population_new) <= population_size:
        population_new.append(population[np.random.randint(0, population_size - 1)])
    population_new = crossover(population_new, Prc, population_size)
    population_new = mutation(population_new, Prm)
    return population_new


if __name__ == '__main__':
    min_weight = 1
    max_weight = 3
    min_value = 1
    max_value = 20
    instances = 100
    weights = np.random.uniform(min_weight, max_weight, instances)
    values = np.random.uniform(min_value, max_value, instances)
    weight_limit = 200
    Prm = 0.001
    Prc = 0.1

    population_size = 300
    population = generate_population(population_size, weights, weight_limit)

    scores = []
    for i in range(0, 1001):
        population = iteration(population, values, weights, weight_limit, population_size, 1/(10*i+1), Prc)
        scores.append(value_from_individual(elitist_selection(population, values, weights, weight_limit, 1)[0], values))


    #plt.plot(scores)
    #plt.show()
