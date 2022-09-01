import numpy as np
import random as rd

from core.network import Network

class BestReproduce:

    def __init__(self, reproduction_function, car, network):
        self.reproduce = reproduction_function
        self.car = car
        self.network = network
    

    def new_car(self, data=[], mutate=False):
        return self.car(network=Network(data=data, mutate=mutate))
        

    def generate(self, population, top_immunity_count, couples_count, top_mutation_factor):
        total_cars = len(population)
        new_grid = list()
        car_count = 0


        # Best individuals are passed to the next generation
        reproduction_pool = list()
        for i in range(top_immunity_count):
            new_grid.append(self.new_car(data=population[i].get_data()))
            reproduction_pool.append(self.new_car(data=population[i].get_data()))
            car_count += 1
            

        # Mutated variants of the best
        for i in range(top_immunity_count):
            for _ in range(top_mutation_factor):
                new_grid.append(self.new_car(data=population[i].get_data(), mutate=True))
                car_count += 1
        

        # Reproduction of the best in the pool 
        rd.shuffle(reproduction_pool)
        for i in range(couples_count):
            children = self.reproduce(reproduction_pool[2*i].network, reproduction_pool[2*i + 1].network)
            new_grid.append(self.new_car(data=children[0]))
            new_grid.append(self.new_car(data=children[1]))
            car_count += 2


        # Adding the rest of the population with mutated individuals
        i = top_immunity_count
        while i < len(population) and car_count < total_cars:
            new_grid.append(self.new_car(data=population[i].get_data(), mutate=True))
            i += 1
            car_count += 1

        # Filling the population with new individuals
        while car_count < total_cars:
            new_grid.append(self.new_car())
            car_count += 1
        
        return new_grid[:total_cars]