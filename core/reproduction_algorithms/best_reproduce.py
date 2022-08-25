import random as rd

class BestReproduce:

    def __init__(self, reproduction_function, new_car):
        self.reproduce = reproduction_function
        self.new_car = new_car


    def generate(self, population, top_immunity_count, couples_count, top_mutation_factor):
        total_cars = len(population)
        new_grid = list()
        car_count = 0

        
        print(f"Old best id: {population[0].id}")
        print(f"Best in original pop:\n{population[0].get_data()[0][0][0]}")


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
        
        print(f"New best id: {new_grid[0].id}")
        print(f"First in new pop:\n{new_grid[0].get_data()[0][0][0]}")

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
        
        return new_grid[:250]