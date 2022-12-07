from neural import NeuralNetwork
import numpy as np
import globals as g
from rocket import Rocket
import random


class Population:
    def __init__(self):
        self.mutation_rate = 0.1
        self.hit = 0  # how many rockets hit the target
        self.generations = 0  # which iteration is this generation on
        self.gen_text = g.font.render(
            f"Generations: {self.generations}", True, (0, 0, 255)
        )  # text to display the generation
        self.hit_text = g.font.render(
            f"Hit last generation: {self.hit}", True, (0, 0, 255)
        )  # text to display the amount of rockets that hit the target
        self.rockets: list[Rocket] = []  # the populations current rockets
        for _ in range(g.max_rockets):
            self.rockets.append(Rocket())  # create the rockets

    def normalize_scores(self):
        total = max([i.score for i in self.rockets])
        for r in self.rockets:
            r.score /= total

    def select_parents(self) -> list[NeuralNetwork]:
        # select the fittest neural networks from the population to be parents
        sorted_population = sorted(self.rockets, key=lambda x: x.score, reverse=True)
        parents = sorted_population[:2]
        return parents

    def reproduce(self):
        """Creates the next generation of rockets."""
        self.normalize_scores()
        parents = self.select_parents()
        new_rockets = []
        for _ in range(g.max_rockets):
            new_net = self.crossover(parents)
            new_rockets.append(Rocket(self.mutate(new_net)))
        self.rockets = new_rockets

    def crossover(self, parents: list[Rocket]) -> NeuralNetwork:
        # create a child neural network by combining the weights of the parents
        child = NeuralNetwork(*g.net_settings)

        child.weights_input_to_hidden = (
            parents[0].net.weights_input_to_hidden
            + parents[1].net.weights_input_to_hidden
        ) / 2
        child.weights_hidden_to_output = (
            parents[0].net.weights_hidden_to_output
            + parents[1].net.weights_hidden_to_output
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

    def update(self, frame: int):
        if frame == g.frames - 1:
            self.generations += 1
            self.gen_text = g.font.render(
                f"Generations: {self.generations}", True, (0, 0, 255)
            )
            self.hit = 0
            for r in self.rockets:
                if r.hit_target:
                    self.hit += 1
                r.eval()
            self.hit_text = g.font.render(
                f"Hit last generation: {self.hit}", True, (0, 0, 255)
            )
            self.reproduce()
        for r in self.rockets:
            r.update(frame)

    def draw(self):
        g.screen.blit(self.gen_text, (0, 0))
        g.screen.blit(self.hit_text, (0, self.gen_text.get_height() - 1))
        for r in self.rockets:
            r.draw()
