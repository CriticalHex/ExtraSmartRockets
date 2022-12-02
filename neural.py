"""Standalone Neural Net Framework"""

from random import randint  # used by custom rand function


def rand(start: int, end: int, *, digits: int = 10):
    """Returns a random number between two numbers to a given amount of digits"""
    d = 10**digits  # a number with as many digits as specified
    s = randint(
        start * d, end * d
    )  # get a random number between the two numbers with as many digits as specified
    return s / d  # return that number scaled back down to starting values


def limit(val: float, min: float, max: float):
    """returns a limited val given a val and the
    numbers that val should be between"""
    if val > max:  # if the number's too big
        return max  # return the numbers max
    if val < min:  # if it's too small
        return min  # return its minimum value
    return val  # otherwise return the number


class Network:
    """Neural Network"""

    class Node:
        """Subclass of Network"""

        def __init__(self, inputs: int) -> None:
            """Creates a node with a list of weights, and a value set to 0"""
            self.weights: list[float] = []
            self.val = 0
            for _ in range(inputs):
                self.weights.append(rand(-1, 1))

        def process(self, inputs: list[float]):
            """Sums all inputs times each associated weight"""
            self.val = 0  # reset val to 0
            for i, input in enumerate(inputs):  # for all inputs
                self.val += input * self.weights[i]  # sum input times weight

    def activate(value: float):
        """Used by the AI to modify output values"""
        return 1 if value >= 0 else -1

    def __init__(
        self, inputs: int, hidden_layers: int, hidden_nodes_per: int, outputs: int
    ) -> None:
        """Creates a neural network with a specified amount of inputs,
        hidden layers, nodes per hidden layers, and output nodes."""
        self.hidden_layers: list[list[Network.Node]] = []
        self.hidden_layers.append(
            [Network.Node(inputs) for _ in range(hidden_nodes_per)]
        )  # add the first hidden layer in which each node takes each input
        for _ in range(hidden_layers - 1):
            self.hidden_layers.append(
                [Network.Node(hidden_nodes_per) for _ in range(hidden_nodes_per)]
            )  # create the rest of the nodes which take the previous layer as inputs
        self.output_nodes = [Network.Node(hidden_nodes_per) for _ in range(outputs)]
        # create the output nodes, which take the last layer of hidden nodes as inputs
        self.output_values: list[float] = []

    def compute(self, inputs: list[float]):
        """Does the AI calculation"""
        # calls the process function of each node one layer at a time
        for layer in self.hidden_layers:
            outputs = []
            # print(f"input: {inputs}")
            for n in layer:
                n.process(inputs)
                outputs.append(n.val)
            inputs = outputs
            # print(f"output: {inputs}")
        self.output_values = []
        # print(f"input: {inputs}")
        for n in self.output_nodes:
            n.process(inputs)
            self.output_values.append(
                Network.activate(n.val)
            )  # conform the final output values
        # print(f"output: {self.output_values}")

    def mutate(self, chance=0.1):
        """with a given chance, modify a nodes weights,
        and keep them bewteen -1 and 1"""
        for layer in self.hidden_layers:
            for n in layer:
                for i in range(len(n.weights)):
                    r = rand(0, 1)
                    if r < chance:
                        n.weights[i] *= rand(-2, 2)
                        n.weights[i] = limit(n.weights[i], -1, 1)
