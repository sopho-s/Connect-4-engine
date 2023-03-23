import random

import GUI
import Neuralnetwork as nnn
import math
from itertools import chain
import pickle
import Montecarlosearch as mcs


def softmax(nums):
    return [math.exp(num) / sum([math.exp(num) for num in nums]) for num in nums]

def train():
    global network
    epochs = 1000 #int(input("How many epochs"))
    evals = 10 #int(input("How many evals per move"))
    alpha = 0.01#float(input("What do you want alpha to be"))
    loss = 0.99#float(input("What do you want loss to be"))
    gameboard = GUI.board()
    network = nnn.network([nnn.layer(nnn.leakyrelu, nnn.leakyreluder, 7*6, 7*6*5), nnn.noise(0.001), nnn.layer(nnn.leakyrelu, nnn.leakyreluder, 7*6*5, 7*6*5), nnn.noise(0.001), nnn.layer(nnn.leakyrelu, nnn.leakyreluder, 7*6*5, 7*6*5), nnn.layer(nnn.sigmoid, nnn.sigmoidder, 7*6*5, 1)], alpha, loss)
    player = 2
    treem = mcs.tree(1, 1, evalposition)
    for epoch in range(epochs):
        updatestotal = []
        print(epoch)
        while not gameboard.check_four_in_a_row():
            if player == 1:
                player = 2
            else:
                player = 1
            for i in range(evals):
                print(i)
                treem.searchnext()
            eval = treem.getevals()
            percentages = softmax(eval)
            cumper = [sum(percentages[i:]) if i != 6 else 0 for i in range(7)]
            print(cumper)
            choice = random.random()
            for i in range(7):
                if choice >= cumper[i]:
                    gameboard.addcounter(i, player);
                    treem, updates = mcs.cuttree(treem, i)
                    if len(updatestotal) == 0:
                        updatestotal = updates
                    else:
                        for t in range(len(updatestotal[1])):
                            updatestotal[1][t] += updates[1][t]
                        for t in range(len(updatestotal[0])):
                            for s in range(len(updatestotal[0][t])):
                                updatestotal[0][t][s] += updates[0][t][s]
                    break
        network.updatelayers(updatestotal)
        with open("network.bin", "wb") as f:
            pickle.dump(network, f)




def evalposition(moves):
    global network
    gameboard = GUI.board()
    player = 1
    for move in moves:
        gameboard.addcounter(move, player)
        if player == 1:
            player = 2
        else:
            player = 1
    board = gameboard.getboard()
    #for row in board:
    #    print(row)
    board = list(chain.from_iterable(board))
    eval = network.run(board)[0]
    #print(eval)
    #print("\n\n")
    network.backprop([1])
    vals = network.getupdatevals()
    isend = gameboard.check_four_in_a_row()
    return eval, vals, isend


train()