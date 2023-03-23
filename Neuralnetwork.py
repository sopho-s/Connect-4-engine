import math
import random

sigmoid = lambda x: 1/(1+math.exp(-x))
sigmoidder = lambda x: (math.exp(x))/((1 + math.exp(x))**2)
tanh = lambda x: ((math.exp(x))-(math.exp(-x)))/((math.exp(x))+(math.exp(x)))
tanhder = lambda x: (4*math.exp(2*x))/((math.exp(2*x) + 1)** 2)
linear = lambda x: x
linearder = lambda x: 1
relu = lambda x: x if x > 0 else 0
reluder = lambda x: 1 if x > 0 else 0
leakyrelu = lambda x: x if x > 0 else x*0.01
leakyreluder = lambda x: 1 if x > 0 else 0.01

class layer:
    def __init__(self, activation, activationder, inputam, outputam):
        self.activation = activation
        self.derivative = activationder
        self.weights = [[random.random() / 100 for _ in range(inputam)] for _ in range(outputam)]
        self.biases = [random.random() / 100 for _ in range(outputam)]
        self.input = []
        self.outputs = [0 for i in range(len(self.biases))]
        self.prevouts = [0 for i in range(len(self.biases))]
        self.previns = [0 for i in range(inputam)]
        self.updatesw = [[0 for _ in range(inputam)] for _ in range(outputam)]
        self.updatesb = [0 for _ in range(outputam)]
    def forwardpass(self, inputs):
        self.previns = inputs
        self.outputs = [0 for i in range(len(self.biases))]
        for outindex, outputw in enumerate(self.weights):
            for inindex, weight in enumerate(outputw):
                self.outputs[outindex] += inputs[inindex] * weight
            self.outputs[outindex] += self.biases[outindex]
            self.outputs[outindex] = self.activation(self.outputs[outindex])
        self.prevouts = self.outputs
        return self.outputs
    def calcupdate(self, contribution, alpha):
        newcontribution = [0 for i in range(len(self.weights[0]))]
        for outindex in range(len(self.weights)):
            grad = self.derivative(self.prevouts[outindex])
            for inindex in range(len(self.weights[outindex])):
                try:
                    self.updatesw[outindex][inindex] = grad * self.weights[outindex][inindex] * self.previns[inindex] * alpha * contribution[outindex]
                    newcontribution[inindex] = grad * self.weights[outindex][inindex] * self.previns[inindex] * contribution[outindex]
                except:
                    print(inindex)
                    print(outindex)
                    print(self.updatesw)
                    print(len(self.updatesw[0]))
                    raise IndexError("hello bitch")
            self.updatesb[outindex] = grad * self.biases[outindex] * alpha * contribution[outindex]
        return newcontribution
    def updatevalues(self, updatesw, updatesb):
        for i in range(len(self.weights)):
            for t in range(len(self.weights[i])):
                self.weights[i][t] += updatesw[i][t]
        for i in range(len(updatesb)):
            self.biases[i] += updatesb[i]
    def getupdatevals(self):
        return self.updatesw, self.updatesb

class noise:
    def __init__(self, alpha):
        self.alpha = alpha
    def forwardpass(self, inputs):
        for i in range(len(inputs)):
            inputs[i] += (random.random()-0.5) * self.alpha
        return inputs
    def calcupdate(self, contribution, _):
        return contribution
    def updatevalues(self, none, _):
        pass
    def getupdatevals(self):
        return [[], []]

class network:
    def __init__(self, layers, alpha, loss):
        self.layers = layers
        self.alpha = alpha
        self.loss = loss
    def run(self, inputs):
        for layer in self.layers:
            inputs = layer.forwardpass(inputs)
        return inputs
    def getupdatevals(self):
        updatevals = []
        for layer in self.layers:
            updatevals.append(layer.getupdatevals())
        return updatevals
    def backprop(self, contribution):
        for i in range(len(self.layers)-1, -1, -1):
            contribution = self.layers[i].calcupdate(contribution, self.alpha)
        self.alpha = self.alpha * self.loss
    def updatelayers(self, updatesvalsl):
        if len(updatesvalsl) != 0:
            for i in range(len(self.layers)):
                self.layers[i].updatesvals(updatesvalsl[i][0], updatesvalsl[i][1])