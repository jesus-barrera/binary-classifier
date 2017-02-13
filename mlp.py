# -*- coding: utf-8 -*-
import sys
import numpy as np

class MultiLayerPerceptron:
    def __init__(self, shape):
        self._shape = shape
        self._outputs_array = []
        self._weights_array = []
        self._net_values = []

        # input layer
        self._weights_array.append(np.zeros(0)) # no weights
        self._net_values.append(np.zeros(0))    # nor net values

        # network input
        inputs = np.zeros(self._shape[0] + 1)
        inputs[0] = -1  # constant input -1 for threshold
        self._outputs_array.append(inputs)

        # hidden layers
        for layer in xrange(1, len(self._shape)):
            # initialize weights
            neurons = self._shape[layer]
            inputs = self._shape[layer - 1] + 1 # threshold
            weights = 2 * np.random.rand(neurons * inputs).reshape((neurons, inputs)) -1 # in (-1, 1)
            self._weights_array.append(weights)

            # initialize outputs
            outputs = np.zeros(neurons + 1)
            outputs[0] = -1
            self._outputs_array.append(outputs)

            # initialize net values
            nets = np.zeros(neurons)
            self._net_values.append(nets)

    def train(
            self,
            training_set,
            learning_rate,
            max_epochs,
            min_error):

        converged = False
        epochs = 0

        while epochs < max_epochs and not converged:
            total_error = 0

            for inputs, desired in training_set:
                # feed feed forward
                self._feed_forward(inputs)

                # compute error
                error = desired - self._outputs_array[-1][1:]
                total_error += error.dot(error) / 2

                # back propagation
                self._back_propagation(error, learning_rate)

            epochs += 1
            total_error /= len(training_set)

            if total_error <= min_error:
                converged = True

        return converged, epochs

    def _feed_forward(self, inputs):
        self._outputs_array[0][1:] = inputs

        for layer in xrange(1, len(self._shape)):
            # previous layer outputs are current layer inputs
            inputs = self._outputs_array[layer - 1]

            # activation values
            self._net_values[layer] = self._weights_array[layer].dot(inputs)

            # compute outputs using activation function
            outputs = self._sigmoid(self._net_values[layer])
            self._outputs_array[layer][1:] = outputs # keep threshold input

    def _back_propagation(self, error, learning_rate):
        sensibilities = [0] * len(self._shape)

        # output layer
        outputs = self._outputs_array[-1][1:]
        derivative = outputs * (1 - outputs)
        sensibility = derivative * error
        sensibility = sensibility.reshape((sensibility.size, 1))

        inputs = self._outputs_array[-2]
        inputs = inputs.reshape((1, inputs.size))

        self._weights_array[-1] += learning_rate * sensibility.dot(inputs)

        sensibilities[-1] = sensibility

        # hidden layers
        for layer in reversed(xrange(1, len(self._shape) - 1)):
            next_layer = layer + 1
            outputs = self._outputs_array[layer][1:]
            derivative = outputs * (1 - outputs)
            derivative = np.diag(derivative)

            weights = self._weights_array[next_layer][:,1:]

            sensibility = weights.T.dot(sensibilities[next_layer])
            sensibility = derivative.dot(sensibility)


            inputs = self._outputs_array[layer - 1]
            inputs = inputs.reshape((1, inputs.size))

            self._weights_array[layer] += learning_rate * sensibility.dot(inputs)

            sensibilities[layer] = sensibility

    def test(self, inputs):
        self._feed_forward(inputs)

        return self._net_values[-1]

    def _sigmoid(self, value):
        return 1 / (1 + np.exp(-value))

if __name__ == '__main__':
    mlp = MultiLayerPerceptron((2, 3, 1))

    training_set = [
        (np.array([0, 0]), np.array([0])),
        (np.array([0, 1]), np.array([1])),
        (np.array([1, 1]), np.array([0])),
        (np.array([1, 0]), np.array([1]))]

    converged, epochs = mlp.train(
            training_set,
            0.3,
            20000,
            0.005)

    if converged:
        print u'La red convergió en {} épocas'.format(epochs)

        print 'Test (0,0) =', mlp.test(np.array([0, 0]))
        print 'Test (1,0) =', mlp.test(np.array([1, 0]))
        print 'Test (1,1) =', mlp.test(np.array([1, 1]))
        print 'Test (0,1) =', mlp.test(np.array([0, 1]))
    else:
        print 'La red no convergió'
