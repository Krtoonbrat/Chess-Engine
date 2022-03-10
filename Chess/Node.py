# class representing a position stored in the transposition table
class Node:
    def __init__(self, type=None, best=None, score=None, pv=None, depth=None):
        self.nodeType = type
        self.bestMove = best
        self.nodeScore = score
        self.PV = pv
        self.nodeDepth = depth
