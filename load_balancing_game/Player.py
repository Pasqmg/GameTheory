"""
Class Player:
    - A player has a name, a job and a weight dictionary
        - The dictionary indicates the cost of the player's job performed by each machine
    - Each turn, the player chooses the best machine to assign its job to, taking into account its cost
"""

import math


class Player:

    def __init__(self, name):
        self.name = name
        self.current_machine = None
        self.new_machine = None
        self.cost = math.inf
        self.job = None
        self.machines = []
        self.weights = {}

    def get_name(self):
        return self.name

    def set_job(self, job):
        self.job = job

    def get_job(self):
        return self.job

    def get_job_cost(self):
        if self.job is not None:
            return self.job.get_cost()

    def set_machines(self, machine_list):
        self.machines = machine_list

    def set_weights(self, weights):
        self.weights = weights

    def get_weight(self, machine_id):
        return self.weights.get(machine_id, -1)

    # The player updates its cost to take into account other players' actions
    def update_cost(self):
        if self.current_machine is not None:
            self.cost = self.current_machine.get_cost()
        else:
            self.cost = math.inf

    # Performs a best-response choice of strategy
    def choose_machine(self):
        # Look for a better machine
        for machine in self.weights.keys():
            # cost = current load of the machine + the cost of my job performed by that machine
            job_cost_in_m = self.weights.get(machine)
            cost = machine.get_cost() + job_cost_in_m
            # if there is a strategy which improves my cost
            if cost < self.cost:
                self.new_machine = machine
                self.cost = cost
        if self.current_machine is None:  # first turn, I still have no machine assigned
            self.current_machine = self.new_machine
            self.current_machine.assign_job(self.job)
        elif self.current_machine != self.new_machine:  # I changed my previous machine to a new one
            self.current_machine.deassign_job(self.job)
            self.current_machine = self.new_machine
            self.current_machine.assign_job(self.job)
        # else: I do no change machine, I do nothing

    """
    CURRENTLY NOT IN USE 
    | | | | | | | | | |
    v v v v v v v v v v 
    """

    # select fastest machine as initial machine
    def first_move(self):
        self.current_machine = self.get_fastest()
        self.current_machine.assign_job(self.job)

    def get_fastest(self):
        fastest = list(self.weights.keys())[0]
        for m in self.weights.keys():
            if m.get_speed() < fastest.get_speed():
                fastest = m
        return fastest
