# import the necessary libraries
import numpy as np

# define the sigmoid function
def sigmoid(x):
  return 1 / (1 + np.exp(-x))

# define the neural network class
class NeuralNetwork:
  def __init__(self, num_inputs, num_hidden, num_outputs):
    # initialize the weights and biases
    self.weights_input_to_hidden = np.random.normal(0, self.hidden_nodes**-0.5,
                                                    (self.hidden_nodes, self.input_nodes))
    self.weights_hidden_to_output = np.random.normal(0, self.output_nodes**-0.5,
                                                     (self.output_nodes, self.hidden_nodes))
    self.bias_hidden = np.zeros((self.hidden_nodes, 1))
    self.bias_output = np.zeros((self.output_nodes, 1))
   
  def train(self, inputs, targets):
    # forward pass
    hidden_inputs = np.dot(self.weights_input_to_hidden, inputs) + self.bias_hidden
    hidden_outputs = sigmoid(hidden_inputs)
    final_inputs = np.dot(self.weights_hidden_to_output, hidden_outputs) + self.bias_output
    final_outputs = sigmoid(final_inputs)
   
    # calculate the error
    output_errors = targets - final_outputs
   
    # backpropagation
    hidden_errors = np.dot(self.weights_hidden_to_output.T, output_errors)
    hidden_grad = hidden_outputs * (1 - hidden_outputs)
    output_grad = final_outputs * (1 - final_outputs)
   
    # update the weights and biases
    self.weights_hidden_to_output += self.learning_rate * np.dot(output_errors * output_grad,
                                                                hidden_outputs.T)
    self.weights_input_to_hidden += self.learning_rate * np.dot(hidden_errors * hidden_grad,
                                                               inputs.T)
    self.bias_hidden += self.learning_rate * hidden_errors * hidden_grad
    self.bias_output += self.learning_rate * output_errors * output_grad
   
  def predict(self, inputs):
    # forward pass
    hidden_inputs = np.dot(self.weights_input_to_hidden, inputs) + self.bias_hidden
    hidden_outputs = sigmoid(hidden_inputs)
    final_inputs = np.dot(self.weights_hidden_to_output, hidden_outputs) + self.bias_output
    final_outputs = sigmoid(final_inputs)
   
    return final_outputs