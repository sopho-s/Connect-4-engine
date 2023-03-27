import math
import time

class tree:
    def __init__(self, currentplayer, simplayer, evaluate):
        self.nodes = []
        self.eval = 0
        self.visits = 1
        self.numcount = [0 for _ in range(7)]
        self.moves = []
        self.explorationparm = 2
        self.currentplayer = currentplayer
        self.simplayer = simplayer
        self.updatevals = []
        self.evalfunc = evaluate
        self.isendstate = False
    def updateeval(self):
        if self.simplayer == 2:
            total = []
            for node in self.nodes:
                if node != None:
                    total.append(node.eval)
                else:
                    total.append(2)
            self.eval = min(total)
        else:
            total = []
            for node in self.nodes:
                if node != None:
                    total.append(node.eval)
                else:
                    total.append(-1)
            self.eval = max(total)
    def changeplayer(self):
        for nodenum in range(len(self.nodes)):
            if self.nodes[nodenum] != None:
                self.nodes[nodenum].changeplayer()
        if self.currentplayer == 1:
            self.currentplayer = 2
        else:
            self.currentplayer = 1
    def evaluate(self):
        self.eval, self.updatevals, self.isendstate = self.evalfunc(self.moves)
    def addnodes(self):
        self.nodes = [tree(self.currentplayer, 1 if self.simplayer == 2 else 2, self.evalfunc) if self.numcount[i] < 6 else None for i in range(7)]
        for i in range(7):
            if self.nodes[i] != None:
                for t in range(len(self.numcount)):
                    self.nodes[i].numcount[t] = self.numcount[t]
                self.nodes[i].numcount[i] += 1
                for move in self.moves:
                    self.nodes[i].moves.append(move)
                self.nodes[i].moves.append(i)
                if self.simplayer == 1:
                    self.nodes[i].simplayer = 2
                else:
                    self.nodes[i].simplayer = 1
                #before = time.time()
                self.nodes[i].evaluate()
                #print(int((time.time() - before)*1000)/1000)
        self.updateeval()
    def upperconfidencebound(self):
        UCB = [None for _ in range(6)]
        for i in range(6):
            if self.nodes[i] != None and not self.nodes[i].isendstate:
                explorationval = self.explorationparm * math.sqrt((math.log(self.visits)) / self.nodes[i].visits)
                UCB[i] = explorationval + self.nodes[i].eval
        return UCB
    def minmax(self, ismax, values):
        if ismax:
            max = 0
            num = -1
            for i in range(len(values)):
                if values[i] != None:
                    if max < values[i]:
                        max = values[i]
                        num = i
            return num
        else:
            min = 10
            num = -1
            for i in range(len(values)):
                if values[i] != None:
                    if min > values[i]:
                        min = values[i]
                        num = i
            return num
    def searchnext(self):
        if len(self.nodes) == 0:
            self.addnodes()
            self.updateeval()
            if all(node == None for node in self.nodes):
                self.isendstate = True
                return False
        else:
            UCB = self.upperconfidencebound()
            if self.simplayer == 1:
                num = self.minmax(True, UCB)
                try:
                    if self.nodes[num].searchnext() == False:
                        if all(node.isendstate == True for node in self.nodes):
                            self.isendstate = True
                            return False
                except:
                    self.isendstate = True
                    return False
            else:
                num = self.minmax(False, UCB)
                try:
                    if self.nodes[num].searchnext() == False:
                        if all(node.isendstate == True for node in self.nodes):
                            self.isendstate = True
                            return False
                except:
                    self.isendstate = True
                    return False
    def returnupdate(self):
        return self.updatevals
    def getevals(self):
        return [node.eval if node != None else 0 for node in self.nodes]

def cuttree(tree, move):
    newtree = tree.nodes[move]
    newtree.changeplayer()
    return newtree, newtree.returnupdate()