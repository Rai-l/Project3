import sys


class PriorityQueue:
    def __init__(self):
        self.queue1 = []
        self.weight1 = 1
        self.weight2 = 0

    def insert(self, edge):
        self.queue1.append(edge)

    def pop(self):
        lowest = ["", sys.maxsize, sys.maxsize]
        index = 0
        for i in range(0, len(self.queue1)):
            if self.priority(self.queue1[i]) <= self.priority(lowest):
                lowest = self.queue1[i]
                index = i
        del self.queue1[index]
        return lowest

    def priority(self, edge):
        priority_val = (edge[1] * self.weight1) + (edge[2] * self.weight2)
        return priority_val

    def empty(self):
        if not self.queue1:
            return True
        return False
