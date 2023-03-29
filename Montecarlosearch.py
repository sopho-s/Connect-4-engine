import math


class tree:
    def __init__(self, currentplayer, simplayer, evaluate):
        self.nodes = []
        self.eval = 0
        self.visits = 1
        self.numcount = [0 for _ in range(7)]
        self.moves = []
        self.exploration_parm = 2
        self.current_player = currentplayer
        self.simplayer = simplayer
        self.update_vals = []
        self.evalfunc = evaluate
        self.is_endstate = False

    def updateeval(self):
        if self.simplayer == 2:
            total = []
            for node in self.nodes:
                if node is not None:
                    total.append(node.eval)
                else:
                    total.append(2)
            self.eval = min(total)
        else:
            total = []
            for node in self.nodes:
                if node is not None:
                    total.append(node.eval)
                else:
                    total.append(-1)
            self.eval = max(total)

    def changeplayer(self):
        for nodenum in range(len(self.nodes)):
            if self.nodes[nodenum] is not None:
                self.nodes[nodenum].changeplayer()
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

    def evaluate(self):
        self.eval, self.update_vals, self.is_endstate = self.evalfunc(self.moves)

    def addnodes(self):
        self.nodes = [
            tree(self.current_player, 1 if self.simplayer == 2 else 2, self.evalfunc) if self.numcount[i] < 6 else None
            for i in range(7)]
        for i in range(7):
            if self.nodes[i] is not None:
                for t in range(len(self.numcount)):
                    self.nodes[i].numcount[t] = self.numcount[t]
                self.nodes[i].numcount[i] += 1
                for move in self.moves:
                    self.nodes[i].moves.append(move)
                self.nodes[i].moves.append(i)
                # before = time.time()
                self.nodes[i].evaluate()
                # print(int((time.time() - before)*1000)/1000)
        self.updateeval()

    def upper_confidence_bound(self):
        UCB = [None for _ in range(6)]
        for i in range(6):
            if self.nodes[i] is not None and not self.nodes[i].is_endstate:
                exploration_val = self.exploration_parm * math.sqrt((math.log(self.visits)) / self.nodes[i].visits)
                UCB[i] = exploration_val + self.nodes[i].eval
        return UCB

    def minmax(self, is_max, values):
        if is_max:
            max = 0
            num = -1
            for i in range(len(values)):
                if values[i] is not None:
                    if max < values[i]:
                        max = values[i]
                        num = i
            return num
        else:
            min = 10
            num = -1
            for i in range(len(values)):
                if values[i] is not None:
                    if min > values[i]:
                        min = values[i]
                        num = i
            return num

    def search_next(self):
        if len(self.nodes) == 0:
            self.addnodes()
            self.updateeval()
            if all(node is None for node in self.nodes):
                self.is_endstate = True
                return False
        else:
            UCB = self.upper_confidence_bound()
            if self.simplayer == 1:
                num = self.minmax(True, UCB)
                try:
                    if not self.nodes[num].search_next():
                        if all(node.is_endstate for node in self.nodes):
                            self.is_endstate = True
                            return False
                except:
                    self.is_endstate = True
                    return False
            else:
                num = self.minmax(False, UCB)
                try:
                    if not self.nodes[num].search_next():
                        if all(node.is_endstate for node in self.nodes):
                            self.is_endstate = True
                            return False
                except:
                    self.is_endstate = True
                    return False

    def returnupdate(self):
        return self.update_vals

    def getevals(self):
        return [node.eval if node is not None else None for node in self.nodes]


def cuttree(tree, move):
    newtree = tree.nodes[move]
    newtree.changeplayer()
    return newtree, newtree.returnupdate()
