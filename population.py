from neural import NeuralNetwork
import numpy as np


class GeneticAlgorithm:
    def __init__(
        self,
        population_size: int,
        mutation_rate: float,
        num_inputs: int,
        num_hidden: int,
        num_outputs: int,
    ):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.num_inputs = num_inputs
        self.num_hidden = num_hidden
        self.num_outputs = num_outputs

    def initialize_population(self) -> list[NeuralNetwork]:
        # initialize a population of neural networks
        population = []
        for i in range(self.population_size):
            nn = NeuralNetwork(self.num_inputs, self.num_hidden, self.num_outputs)
            population.append(nn)
        return population

    def calculate_fitness(
        self,
        population: list[NeuralNetwork],
        inputs: list[list[float]],
        expected_outputs: list[list[float]],
    ):
        # calculate the fitness of each neural network in the population
        for nn in population:
            outputs = nn.forward_propagation(inputs)
            error = np.mean((expected_outputs - outputs) ** 2)
            nn.fitness = 1 / (1 + error)

    def select_parents(self, population: list[NeuralNetwork]) -> list[NeuralNetwork]:
        # select the fittest neural networks from the population to be parents
        sorted_population = sorted(population, key=lambda x: x.fitness, reverse=True)
        parents = sorted_population[:2]
        return parents

    def crossover(self, parents: list[NeuralNetwork]) -> NeuralNetwork:
        # create a child neural network by combining the weights of the parents
        child = NeuralNetwork(self.num_inputs, self.num_hidden, self.num_outputs)

        child.weights_input_to_hidden = (
            parents[0].weights_input_to_hidden + parents[1].weights_input_to_hidden
        ) / 2
        child.weights_hidden_to_output = (
            parents[0].weights_hidden_to_output + parents[1].weights_hidden_to_output
        ) / 2

        return child

    def mutate(self, child: NeuralNetwork) -> NeuralNetwork:
        # randomly mutate the weights of the child neural network
        child.weights_input_to_hidden += np.random.normal(
            0, self.mutation_rate, child.weights_input_to_hidden.shape
        )
        child.weights_hidden_to_output += np.random.normal(
            0, self.mutation_rate, child.weights_hidden_to_output.shape
        )

        return child
