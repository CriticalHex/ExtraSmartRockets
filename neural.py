from random import randint, random


def rand(start: int, end: int, *, digits: int = 10):
    d = 10**digits
    s = randint(start * d, end * d)
    return s / d


# def activate(guess: float):
#     return 1 if guess >= 0 else -1


def activate(guess: float):
    if guess >= 0:
        return 1
    if guess < 0:
        return -1
    print("WHAT")


class Network:
    class Node:
        def __init__(self, inputs: int) -> None:
            self.weights: list[float] = []
            for _ in range(inputs):
                self.weights.append(rand(-1, 1))
            self.val = 0

        def process(self, inputs: list[float]):
            for i, input in enumerate(inputs):
                self.val += input * self.weights[i]

    def __init__(self, inputs: int, hidden_nodes: int, outputs: int) -> None:
        self.hidden_nodes = [Network.Node(inputs) for _ in range(hidden_nodes)]
        self.output_nodes = [Network.Node(hidden_nodes) for _ in range(outputs)]
        self.hidden_values: list[float] = []
        self.output_values: list[float] = []

    def compute(self, inputs: list[float]):
        self.hidden_values = []
        for h in self.hidden_nodes:
            h.process(inputs)
            self.hidden_values.append(h.val)
        self.output_values = []
        for o in self.output_nodes:
            o.process(self.hidden_values)
            self.output_values.append(o.val)
        print(len(self.output_values))

    def mutate(self, chance=0.1):
        for n in self.hidden_nodes:
            for i in range(len(n.weights)):
                r = random()
                if r < chance:
                    n.weights[i] = rand(-1, 1)
