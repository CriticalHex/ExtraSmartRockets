import numpy as np

class NeuralNetwork:
    def __init__(self, num_inputs, num_hidden, num_outputs):
        self.num_inputs = num_inputs
        self.num_hidden = num_hidden
        self.num_outputs = num_outputs

        # initialize weights randomly with a mean of 0
        self.weights_input_to_hidden = np.random.normal(0, self.num_inputs**-0.5, 
                                       (self.num_inputs, self.num_hidden))

        self.weights_hidden_to_output = np.random.normal(0, self.num_hidden**-0.5, 
                                       (self.num_hidden, self.num_outputs))

    def sigmoid(self, x):
        # apply sigmoid activation function
        return 1 / (1 + np.exp(-x))

    def forward_propagation(self, inputs):
        # convert inputs to a 2d array
        inputs = np.array(inputs, ndmin=2).T

        # hidden layer
        hidden_inputs = np.dot(self.weights_input_to_hidden.T, inputs)
        hidden_outputs = self.sigmoid(hidden_inputs)

        # output layer
        final_inputs = np.dot(self.weights_hidden_to_output.T, hidden_outputs)
        final_outputs = self.sigmoid(final_inputs)

        return final_outputs


class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate, num_inputs, num_hidden, num_outputs):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.num_inputs = num_inputs
        self.num_hidden = num_hidden
        self.num_outputs = num_outputs

    def initialize_population(self):
        # initialize a population of neural networks
        population = []
        for i in range(self.population_size):
            nn = NeuralNetwork(self.num_inputs, self.num_hidden, self.num_outputs)
            population.append(nn)
        return population

    def calculate_fitness(self, population, inputs, expected_outputs):
        # calculate the fitness of each neural network in the population
        for nn in population:
            outputs = nn.forward_propagation(inputs)
            error = np.mean((expected_outputs - outputs)**2)
            nn.fitness = 1 / (1 + error)
    
    def select_parents(self, population):
        # select the fittest neural networks from the population to be parents
        sorted_population = sorted(population, key=lambda x: x.fitness, reverse=True)
        parents = sorted_population[:2]
        return parents

    def crossover(self, parents):
        # create a child neural network by combining the weights of the parents
        child = NeuralNetwork(self.num_inputs, self.num_hidden, self.num_outputs)

        child.weights
