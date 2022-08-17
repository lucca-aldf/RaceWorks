import numpy as np
import random as rd
import math

'''
The neural network is to be arranged in an input layer with XXXXXXXXXX inputs, three hidden layers of eight fully-conected neurons each, and two outputs. The weights of the network will be stored in a tridimensional array, with the first dimension being the layers, the second being every neuron, and the third the weights for every following connection. Furthermore, a one-dimensional array containing the biases to be passed along to the nex layer will also be provided. Note that the output layer has no weights, and to ensure the integrity of the network a one-dimensional array with all the layer's sizes will be provided

'''


rd.seed(20062002)

def random_weight():
    return rd.random() * rd.choice([-1,1])

class Network:

    network_structure = np.array([9,8,8,8,2])

    # Mutation explained later in the code
    mutation_chance = 0.04              # Chance for each parameter to mutate when network ordered to mutate
    mutation_strength = 1.01 * 1000     # How large the alterations to the value of the weight can be
    mutation_noise = 0.01             # Addition factor


    def weight_mutation():
        return math.pow(rd.randrange(start=1000, stop=Network.mutation_strength, step=1) / 1000, rd.choice([-1, 1]))

    def weight_noise():
        return rd.random() * rd.choice([-1,1])


    def __init__(self, data=[], mutate=False):
        
        if len(data) == 0:
            self.network_weights = np.array([[[random_weight() for k in range(self.network_structure[i+1])] for j in range(self.network_structure[i])] for i in range(len(self.network_structure) - 1)])
            
        
        else:
            self.network_weights = data

            if mutate:
                self.mutate()

    def feedforward(self, data):
        for layer in range(len(self.network_weights)):
            data = np.dot(data, self.network_weights[layer])

        return data.flatten()


    def mutate(self):
        x = self.network_weights.copy()
        for layer in range(len(self.network_weights)):
            for neuron in range(len(self.network_weights[layer])):
                for weight in range(len(self.network_weights[layer][neuron])):

                    if rd.random() < self.mutation_chance: # If mutation happens
                        self.network_weights[layer][neuron][weight] = self.network_weights[layer][neuron][weight] * Network.weight_mutation() + Network.weight_noise()
