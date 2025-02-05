import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog
import os, sys
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from pandas import DataFrame
from matplotlib.backend_bases import key_press_handler
from tkinter import *
from numba import jit

#############Define some defaut values only for testing###############
global stop
global learning_coeficient
global load
global percentage
percentage =1
load =0


learning_coeficient=int(sys.argv[2])
stop=int(sys.argv[1])
##################################################

plot_list=[]

for i in range (stop*learning_coeficient):
    plot_list.append(i)
# defining some numbers for chart
# just dont care and continue

class NeuralNetwork():

    def __init__(self):
        np.random.seed(1)
        if load==1:
            self.synaptic_weights=np.load('synaptic_weights.npy', mmap_mode=None, allow_pickle=False, fix_imports=True, encoding='ASCII')
            print('only once')
        else:
            self.synaptic_weights = 2*np.random.random((50,1))-1

        self.error_history = []


    def sigmoid(self, x, deriv=False):
        if deriv == True:
            return x * (1 - x)
        return 1/(1+np.exp(-x))

    def backpropagation(self):
        self.error  = self.outputs - self.hidden
        delta = self.error * self.sigmoid(self.hidden, deriv=True)
        self.weights += np.dot(self.inputs.T, delta)


    def train(self, training_inputs, training_outputs, training_iterations):

        for iteration in range(training_iterations*learning_coeficient):

            output= self.think(training_inputs)

            self.error = training_outputs-output
            self.chyba=(self.error/(output/100))
            self.error_history.append(np.average(np.abs(self.chyba)))

            adjustments = np.dot(training_inputs.T, self.error*self.sigmoid(output, deriv=True))

            self.synaptic_weights = self.synaptic_weights + adjustments
            if load ==0:
                cosi=(np.average(np.abs(self.chyba)))
                if cosi<percentage:
                    np.save('synaptic_weights', self.synaptic_weights, allow_pickle=True, fix_imports=True)


    def think(self, inputs):

        inputs = inputs.astype(float)
        output = self.sigmoid(np.dot(inputs, self.synaptic_weights))

        return output

if __name__ == "__main__":

    neural_network = NeuralNetwork()

    ################################
    #
    #       KONSTANTY
    #
    ################################

    pocet_uceni = 1
    pocet_vstupu = 50

    #print("Random synaptic weights: ")
    #print(neural_network.synaptic_weights)


########### Nacitani vstupu ze souboru #########################
    cwd = os.getcwd()
    str=(cwd+'\\ropa.txt')
    f = open(str, "r")
#################################################################
    data = list()


    for i in range(8308): #8308
        line = f.readline()
        data.append(float(line))
        #print(data[i])


    training_inputs = np.empty([3,50])

    for pozice in range((len(data)-pocet_vstupu-250)):
        for i in range(pocet_vstupu):
            training_inputs[0][i] = data[pozice+i]
        for i in range(pocet_vstupu):
            training_inputs[1][i] = data[pozice+i+1]
        for i in range(pocet_vstupu):
            training_inputs[2][i] = data[pozice+i+2]

        #print("testovací sady:")
        #print(training_inputs)
        print("traning ", pozice, "/8000")


##############stoping for export weights && ploting chart#############
        if(pozice == stop):
            print('DONE')
            np.save('error_history', neural_network.error_history, allow_pickle=True, fix_imports=True)
            np.save('plot_list', plot_list, allow_pickle=True, fix_imports=True)
            exit()

##########################################################################


        training_outputs = np.array([data[pozice+pocet_vstupu+1],data[pozice+pocet_vstupu+2],data[pozice+pocet_vstupu+3]]).T
        neural_network.train(training_inputs, training_outputs, pocet_uceni)

    print("TEST")
    print("Synaptic weights after training: ")
    #print(neural_network.synaptic_weights)


    ###################
    #    TESTOVACÍ DATA
    ###################

    testovaci_data = np.empty(50)
    for i in range(50):
        testovaci_data[i] = data[8200+i]
    print("Expected value for this testing input:")
    print(data[8200+i+1])


    print("New situation:")
    #print(neural_network.synaptic_weights)
    print("Output data = ")
    print(neural_network.think(testovaci_data))
