from random import randint


def rand(start: int, end: int, *, digits: int = 10):
    d = 10**digits
    s = randint(start * d, end * d)
    return s / d


class Network:
    class Node:
        def __init__(self, inputs: int) -> None:
            self.weights = []
            for _ in range(inputs):
                self.weights.append(rand(-1, 1))
            self.val = 0

        def process(self, inputs: list[float]):
            for input, i in enumerate(inputs):
                self.val += input * self.weights[i]

    def __init__(self, inputs: int, hidden_nodes: int, outputs: int) -> None:
        self.inputs = [None for _ in range(inputs)]
        self.hidden_nodes = [Network.Node(inputs) for _ in range(hidden_nodes)]
        self.output_nodes = [Network.Node(hidden_nodes) for _ in range(outputs)]
        self.hidden_values = []
        self.output_values = []

    def compute(self):
        self.hidden_values = []
        for h in self.hidden_nodes:
            h.process(self.inputs)
            self.hidden_values.append[h.val]
        self.output_values = []
        for o in self.output_nodes:
            o.process(self.hidden_values)
            self.output_values.append[self.activate(o.val)]

    def activate(guess: float):
        return 1 if guess >= 0 else -1