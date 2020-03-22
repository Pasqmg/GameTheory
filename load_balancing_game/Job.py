import random


class Job:

    def __init__(self, name, machine_amount):
        self.name = name
        self.weight = random.randint(5,11)
