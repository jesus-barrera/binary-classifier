import numpy as np

class MultiLayerPerceptron:
    def __init__(self, input_size, shape):
        self.shape = shape
        self.input_size = input_size
        self.outputs_array = []
        self.weights_array = []
        self.activation_values = []

        # initialize weights
        self.add_layer(self.shape[0], input_size)

        for i in xrange(1, len(shape)):
            self.add_layer(self.shape[i], self.shape[i - 1])

        # initialize outputs
        for i, neurons in enumerate(shape):
            self.outputs_array.append(np.zeros(neurons))
            self.activation_values.append(np.zeros(neurons))

    def add_layer(self, neurons, input_size):
        weights = np.random.random((neurons, input_size + 1))
        self.weights_array.append(weights)

    def train(
            self,
            training_set,
            learning_rate=0.1,
            min_error=0.1):

        done = False

        for i in range(200):
            for inputs, output in training_set:
                self.feed_forward(inputs)

                error = output - self.outputs_array[:-1]
                self.back_propagation(output, learning_rate)

    def feed_forward(self, inputs):
        # compute first layer outputs
        first_layer, = self.shape
        self.compute_layer_outputs(first_layer, inputs)

        for layer in xrange(1, len(self.shape)):
            self.compute_layer_outputs(layer, self.outputs[layer - 1])

    def compute_layer_outputs(self, layer, inputs):
        for neuron in range(self.shape[layer]):
            # set output
            value = np.dot(inputs, self.weights_array[layer][neuron])
            self.outputs_array[layer][neuron] = self.sigmoid(value)

            # save activation value
            self.activation_values[layer][neuron] = value

    def back_propagation(self, error, learning_rate):
        sensibilities = []

        # last layer sensibility
        a = self.diff_sigmoid(self.activation_values[0])
        a = np.diag(a)

        s = -2 * np.dot(a, error)

        self.weights_array[:-1] += -self.learning_rate * np.dot(s, self.outputs[:-2])

        sensibilities.append(s)

        for layer in reversed(range(len(self.shape) - 1)):
            # last layer sensibility
            a = self.diff_sigmoid(self.activation_values[layer])
            a = np.diag(a)

            s = np.dot(a, self.weights_array[layer + 1].T)
            s = np.dot()

            self.weights_array[-1] += -self.learning_rate * np.dot(s, self.outputs[-2])

            sensibilities.append(s)

    def test(self, inputs):
        self.feed_forward(inputs)

        return self.activation_values[:-1]

    def sigmoid(self, value):
        return 1 / (1 + np.exp(-value))

    def diff_sigmoid(self, value):
        return self.sigmoid(value) * (1 - self.sigmoid(value))

if __name__ == '__main__':
    mlp = MultiLayerPerceptron(3, (5, 5))
