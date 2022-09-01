import numpy as np
import random as rd
import math

'''
The neural network is to be arranged in an input layer with XXXXXXXXXX inputs, three hidden layers of eight fully-conected neurons each, and two outputs. The weights of the network will be stored in a tridimensional array, with the first dimension being the layers, the second being every neuron, and the third the weights for every following connection. Furthermore, a one-dimensional array containing the biases to be passed along to the nex layer will also be provided. Note that the output layer has no weights, and to ensure the integrity of the network a one-dimensional array with all the layer's sizes will be provided

'''


rd.seed(20062002)

def sigmoid(x):
    return 1 / (1 + math.exp(-x))


class Network:

    id_counter = 0

    network_structure = np.array([8,6,4,4])

    # Mutation explained later in the code
    individual_mutation_chance = 0           # Chance for each network to mutate when ordered to mutate
    crossover_chance = 0.8                      # Crossover chance
    crossover_bias = 0.5                        # How likely it is for the genes to be picked from one over the other parent
    gene_mutation_chance = 0                  
    mutation_strength_factor = 0.1 * 1000 + 1000# How large the alterations to the value of the weight can be
    mutation_noise_factor = 1000                 # Addition factor


    def set_individual_mutation_chance(n):
        Network.individual_mutation_chance = n
    def set_crossover_chance(n):
        Network.crossover_chance = n
    def set_crossover_bias(n):
        Network.crossover_bias = n
    def set_gene_mutation_chance(n):
        Network.gene_mutation_chance = n
    def set_mutation_strength_factor(n):
        Network.mutation_strength_factor = n * 1000 + 1000
    def set_mutation_noise_factor(n):
        Network.mutation_noise_factor = n

    
    def init_random_weight():
        return rd.random() * rd.choice([-1,1])

    def weight_mutation():
        return math.pow(rd.randrange(start=1000, stop=Network.mutation_strength_factor, step=1) / 1000, rd.choice([-1, 1])) * rd.choice([-1,1])

    def weight_noise():
        return rd.random() * rd.choice([-1,1])

    
    def reproduce(parent_A, parent_B):

        child_A, child_B = Network(parent_A.get_data()), Network(parent_B.get_data())
        
        if rd.random() < Network.crossover_chance:

            for layer in range(len(parent_A.network_weights)):
                for neuron in range(len(parent_A.network_weights[layer])):
                    for weight in range(len(parent_A.network_weights[layer][neuron])):

                        if rd.random() < Network.crossover_bias:
                            child_A.network_weights[layer][neuron][weight] = parent_A.network_weights[layer][neuron][weight]
                            child_B.network_weights[layer][neuron][weight] = parent_B.network_weights[layer][neuron][weight]
                        else:
                            child_A.network_weights[layer][neuron][weight] = parent_B.network_weights[layer][neuron][weight]
                            child_B.network_weights[layer][neuron][weight] = parent_A.network_weights[layer][neuron][weight]

            for layer in range(len(parent_A.bias)):
                if rd.random() < Network.crossover_bias:
                    child_A.bias[layer] = parent_A.bias[layer]
                    child_B.bias[layer] = parent_B.bias[layer]

                else:
                    child_A.bias[layer] = parent_B.bias[layer]
                    child_B.bias[layer] = parent_A.bias[layer]

        return child_A.get_data(), child_B.get_data()


    def __init__(self, data=[], mutate=False):

        if len(data) == 0:
            self.network_weights = np.array([[[Network.init_random_weight() for k in range(self.network_structure[i+1])] for j in range(self.network_structure[i])] for i in range(len(self.network_structure) - 1)]) # Returns a numpy array in the specified architecture
            
            self.bias = np.array([Network.init_random_weight() for i in range(len(self.network_structure) - 1)])
            
            self.id = [Network.id_counter]
            Network.id_counter += 1

        else: # Copy of previous individual
            network_weights, bias, self.id = data

            self.network_weights = np.array([[[network_weights[i][j][k] for k in range(self.network_structure[i+1])] for j in range(self.network_structure[i])] for i in range(len(self.network_structure) - 1)])

            self.bias = np.array([bias[i] for i in range(len(self.network_structure) - 1)])

            if mutate:
                self.id.append(Network.id_counter)
                Network.id_counter += 1
                self.mutate()


    def get_data(self):
        return [self.network_weights.copy(), np.copy(self.bias), self.id.copy()]

    def feedforward(self, data):
        for layer in range(len(self.network_weights)):
            data = np.dot(data, self.network_weights[layer])
            data = np.clip(data, -500, 500)
            for i in range(len(data)):
                data[i] = sigmoid(data[i]) + self.bias[layer]

        data = data.flatten()
        return [data[0] - data[1], data[2] - data[3]]

    def mutate(self):
        if rd.random() < Network.individual_mutation_chance:

            for layer in range(len(self.network_weights)):
                for neuron in range(len(self.network_weights[layer])):
                    for weight in range(len(self.network_weights[layer][neuron])):

                        if rd.random() < Network.gene_mutation_chance: # If mutation happens
                            self.network_weights[layer][neuron][weight] = self.network_weights[layer][neuron][weight] * Network.weight_mutation() + Network.weight_noise()

            for layer in range(len(self.bias)):
                self.bias[layer] = self.bias[layer] * Network.weight_mutation() + Network.weight_noise()