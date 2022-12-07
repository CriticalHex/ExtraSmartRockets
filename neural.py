import numpy as np


class NeuralNetwork:
    def __init__(self, num_inputs: int, num_hidden: int, num_outputs: int):
        self.num_inputs = num_inputs
        self.num_hidden = num_hidden
        self.num_outputs = num_outputs

        # initialize weights randomly with a mean of 0
        self.weights_input_to_hidden = np.random.normal(
            0, self.num_inputs**-0.5, (self.num_inputs, self.num_hidden)
        )

        self.weights_hidden_to_output = np.random.normal(
            0, self.num_hidden**-0.5, (self.num_hidden, self.num_outputs)
        )

    def sigmoid(self, x: np.ndarray) -> np.ndarray:
        # apply sigmoid activation function
        # return 1 / (1 + np.exp(-x))
        return np.arctan(x.astype(np.float64))

    def forward_propagation(self, inputs: list[float]) -> None:
        # convert inputs to a 2d array
        inputs = np.array(inputs, ndmin=2, dtype=object).T

        # hidden layer
        hidden_inputs = np.dot(self.weights_input_to_hidden.T, inputs)
        hidden_outputs = self.sigmoid(hidden_inputs)

        # output layer
        final_inputs = np.dot(self.weights_hidden_to_output.T, hidden_outputs)
        self.final_outputs = self.sigmoid(final_inputs)
