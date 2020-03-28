import random


class Job:

    def __init__(self, player, cost, id=None):
        self.id = id
        self.owner = player
        self.cost = cost

    def set_player(self, player):
        self.owner = player

    def get_cost(self):
        return self.cost

    def print(self):
        return "<" + str(self.owner), str(self.cost) + ">"
