import math


# A tree that searches for the best move to make
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
        """
        If the current player is player 2, then the evaluation of the current node is the minimum of the evaluations of its
        children. Otherwise, the evaluation of the current node is the maximum of the evaluations of its children
        """
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
        """
        It changes the current player to the other player
        """
        for nodenum in range(len(self.nodes)):
            if self.nodes[nodenum] is not None:
                self.nodes[nodenum].changeplayer()
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

    def evaluate(self):
        """
        evaluate evaluates the current state of the game, and returns a tuple of the evaluation, the updated values, and
        whether or not the game is over.
        """
        self.eval, self.update_vals, self.is_endstate = self.evalfunc(self.moves)

    def addnodes(self):
        """
        It creates a new node for each possible move, and then evaluates the board
        """
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
        """
        The function takes the current node and returns a list of the UCB values for each of the child nodes
        :return: The upper confidence bound for each of the 6 possible actions.
        """
        UCB = [None for _ in range(6)]
        for i in range(6):
            if self.nodes[i] is not None and not self.nodes[i].is_endstate:
                exploration_val = self.exploration_parm * math.sqrt((math.log(self.visits)) / self.nodes[i].visits)
                UCB[i] = exploration_val + self.nodes[i].eval
        return UCB

    def minmax(self, is_max, values):
        """
        If is_max is True, return the index of the maximum value in values. If is_max is False, return the index of the
        minimum value in values

        :param is_max: True if we want to find the maximum value, False if we want to find the minimum value
        :param values: a list of values to be evaluated
        :return: The index of the max or min value in the list.
        """
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
        """
        If there are no nodes, add nodes, update the evaluation, and if all nodes are None, set the endstate to True and
        return False. Otherwise, find the UCB, and if the simplayer is 1, find the minmax of True and UCB, and if the node
        is not the endstate, if all nodes are endstates, set the endstate to True and return False. Otherwise, if the
        simplayer is not 1, find the minmax of False and UCB, and if the node is not the endstate, if all nodes are
        endstates, set the endstate to True and return False
        :return: the number of the node that is being searched.
        """
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
        """
        It returns a list of the evaluation of each node in the list of nodes, or None if the node is None
        :return: A list of the evaluations of the nodes in the tree.
        """
        return [node.eval if node is not None else None for node in self.nodes]


def cuttree(tree, move):
    """
    It takes a tree and a move, and returns a new tree and a list of updates

    :param tree: the tree you want to cut
    :param move: the move you want to make
    :return: The new tree and the update.
    """
    newtree = tree.nodes[move]
    newtree.changeplayer()
    return newtree, newtree.returnupdate()
