import random
import pygame

import GUI
import Neuralnetwork as nnn
import math
from itertools import chain
import pickle
import Montecarlosearch as mcs
import dill
import Trainingdatavis as tdv

def softmax(nums):
    return [math.exp(num) / sum([math.exp(num) for num in nums]) for num in nums]
def calcdraw(board):
    isdraw = True
    for column in board:
        for value in column:
            if value == 0:
                isdraw = False
                break
    return isdraw
def train():
    global network
    epochs = 10000#int(input("How many epochs"))
    evals = 100#int(input("How many evals per move"))
    alpha = 1#float(input("What do you want alpha to be"))
    loss = 0.99#float(input("What do you want loss to be"))
    gameboard = GUI.board()
    player1wins = 0
    player2wins = 0
    datavis = tdv.datavis()
    try:
        with open("network.bin", "rb") as f:
            network = dill.load(f)
    except:
        network = nnn.network([nnn.layer(nnn.swish, nnn.swishder, 7*6, 7*6, 0.1), nnn.noise(0.01), nnn.layer(nnn.swish, nnn.swishder, 7*6, 7*6, 0.1), nnn.noise(0.01), nnn.layer(nnn.sigmoid, nnn.sigmoidder, 7*6, 1, 0.1)], alpha, loss)
    try:
        with open("datavis.bin", "rb") as f:
            datavis = pickle.load(f)
    except:
        pass
    for epoch in range(epochs):
        player = 2
        treem = mcs.tree(1, 1, evalposition)
        gameboard.reset()
        updatestotal = []
        print(epoch)
        evalss = []
        isdraw = False
        curveval = 0
        while not (gameboard.check_four_in_a_row() or isdraw):
            preveval = curveval
            if player == 1:
                player = 2
            else:
                player = 1
            for i in range(evals):
                treem.searchnext()
            eval = treem.getevals()
            if player == 2:
                eval = [1-ev if ev != None else 0 for ev in eval]
            else:
                eval = [ev if ev != None else 0 for ev in eval]
            for i in range(len(eval)):
                eval[i] = eval[i] * 30
            percentages = softmax(eval)
            cumper = [sum(percentages[i+1:]) if i != 6 else 0 for i in range(7)]
            #print(cumper)
            chosen = False

            while not chosen:
                choice = random.random()
                for i in range(7):
                    if choice >= cumper[i]:
                        if gameboard.addcounter(i, player):
                            #print("board evaluation is ", '%.3g' % treem.eval)
                            curveval = treem.getnext()
                            evalss.append(treem.eval)
                            treem, updates = mcs.cuttree(treem, i)
                            if len(updatestotal) == 0 and updates != None:
                                updatestotal = updates
                            else:
                                if updates != None:
                                    for t in range(len(updatestotal[1])):
                                        updatestotal[1][t] += updates[1][t]
                                    for t in range(len(updatestotal[0])):
                                        for s in range(len(updatestotal[0][t])):
                                            updatestotal[0][t][s] += updates[0][t][s]
                            chosen = True
                            break
            board = gameboard.getboard()
            isdraw = calcdraw(board)
        if not isdraw:
            if player == 1:
                result = 1
            else:
                result = -1
        else:
            result = 0
        datavis.adddata(preveval, evalss, result)
        player1wins += result if result > 0 else 0
        player2wins += -result if result < 0 else 0
        network.updatelayers(updatestotal, result)
        print("player one has won: ", player1wins)
        print("player two has won: ", player2wins)
        if epoch % 10 == 0:
            with open("network.bin", "wb") as f:
                dill.dump(network, f)
            with open("datavis.bin", "wb") as f:
                pickle.dump(datavis, f)
def play():
    global network
    player = 1
    evals = 200
    gameboard = GUI.board()
    treem = mcs.tree(1, 1, evalposition)
    gameboard.reset()
    isdraw = False
    alpha = 0
    loss = 0
    network = nnn.network([nnn.layer(nnn.swish, nnn.swishder, 7*6, 7*6), nnn.noise(0.01), nnn.layer(nnn.swish, nnn.swishder, 7*6, 7*6), nnn.noise(0.01), nnn.layer(nnn.swish, nnn.swishder, 7*6, 7*6), nnn.layer(nnn.swish, nnn.swishder, 7*6, 7*6), nnn.layer(nnn.swish, nnn.swishder, 7*6, 7*6), nnn.layer(nnn.swish, nnn.swishder, 7*6, 7*6), nnn.layer(nnn.swish, nnn.swishder, 7*6, 7*6), nnn.layer(nnn.swish, nnn.swishder, 7*6, 7*6), nnn.layer(nnn.sigmoid, nnn.sigmoidder, 7*6, 1)], alpha, loss)
    with open("A:/RL/connect4/network.bin", "rb") as f:
        network = dill.load(f)
    playerofuser = int(input("which player do you wish to be"))
    pygame.init()
    pygame.display.set_caption("connect 4")

    screen = pygame.display.set_mode((700,600))

    running = True

    while running:
        while not (gameboard.check_four_in_a_row() or isdraw):
            if player != playerofuser:
                for i in range(evals):
                    treem.searchnext()
                eval = treem.getevals()
                if player == 2:
                    eval = [1-ev if ev != None else 0 for ev in eval]
                else:
                    eval = [ev if ev != None else 0 for ev in eval]
                for i in range(len(eval)):
                    eval[i] = eval[i] * 30
                chosen = False
                notchooselist = []
                while not chosen:
                    max = 0
                    t = 0
                    index = 0
                    for value in eval:
                        if max < value and not index in notchooselist:
                            index = t
                            max = value
                        t += 1
                    if gameboard.addcounter(index, player):
                        print(6-index)
                        print(treem.eval)
                        print("\n\n\n")
                        treem, updates = mcs.cuttree(treem, index)
                        chosen = True
                    notchooselist.append(index)
                if player == 1:
                    player = 2
                else:
                    player = 1
                for rectangle in gameboard.getrects():
                    pygame.draw.rect(screen, rectangle[0], rectangle[1])
                pygame.display.flip()
                pygame.display.update()
            else:
                while player == playerofuser:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pos = GUI.user_click()
                            if gameboard.addcounter(pos, player) != False:
                                treem.searchnext()
                                treem, updates = mcs.cuttree(treem, pos)
                                for rectangle in gameboard.getrects():
                                    pygame.draw.rect(screen, rectangle[0], rectangle[1])
                                pygame.display.flip()
                                pygame.display.update()
                                if player == 1:
                                    player = 2
                                else:
                                    player = 1
            board = gameboard.getboard()
            isdraw = calcdraw(board)
        running = False


def evalposition(moves):
    global network
    gameboard = GUI.board()
    player = 2
    for move in moves:
        if player == 1:
            player = 2
        else:
            player = 1
        gameboard.addcounter(move, player)
    board = gameboard.getboard()
    isend = False
    if gameboard.check_four_in_a_row():
        isend = True
        if player == 2:
            eval = 0
        else:
            eval = 1
        vals = None
    elif calcdraw(board):
        isend = True
        eval = 0.5
        vals = None
    else:
        board = list(chain.from_iterable(board))
        eval = network.run(board)[0]
        network.backprop([1])
        vals = network.getupdatevals()
    return eval, vals, isend


train()