import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pickle

class datavis:
    def __init__(self):
        self.player1wineval = []
        self.player2wineval = []
        self.draweval = []
        self.evals = []
        self.evalbeforeend = []
        self.dwl = []
    def adddata(self, evalbeforeend, evals, playerwin):
        self.dwl.append(playerwin)
        self.evalbeforeend.append(evalbeforeend)
        self.evals.append(evals)
        if playerwin == 1:
            self.player1wineval.append(evals)
        elif playerwin == -1:
            self.player2wineval.append(evals)
        else:
            self.draweval.append(evals)
    def dwlshow(self):
        result = [0, 0, 0]
        for value in self.dwl:
            if value == 1:
                result[0] += 1
            elif value == 0:
                result[1] += 1
            else:
                result[2] += 1
        fig, ax = plt.subplots()
        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True
        plt.barh(["w/d/l"], [result[0]], height=1, color="green")
        plt.barh(["w/d/l"], [result[1]], height=1, left=[result[0]], color="yellow")
        plt.barh(["w/d/l"], [result[2]], height=1, left=[result[0]+result[1]], color="red")
        plt.show()
    def evalbeforeshow(self):
        fig, axs = plt.subplots(3, 1, sharex=True)
        fig.subplots_adjust(hspace=0)
        player1 = []
        player2 = []
        draw = []
        for i in range(len(self.evalbeforeend)):
            if self.dwl[i] == 1:
                player1.append(self.evalbeforeend[i])
            elif self.dwl[i] == -1:
                player2.append(self.evalbeforeend[i])
            else:
                draw.append(self.evalbeforeend[i])
        axs[0].plot(player1)
        axs[1].plot(draw)
        axs[2].plot(player2)
        plt.show()

def loadandtest():
    datav = datavis()
    with open("datavis.bin", "rb") as f:
        datav = pickle.load(f)
    datav.dwlshow()
    datav.evalbeforeshow()
loadandtest()