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

    def set_job(self, job):
        self.job = job

    def set_machines(self, machine_list):
        self.machines = machine_list

    def set_weights(self, weights):
        self.weights = weights

    def get_weight(self, machine_id):
        return self.weights.get(machine_id, -1)

    '''
    Checks all machines and chooses to assign its job to, according to cost
    '''
    def choose_machine(self):
        for machine in self.weights.keys():
            # cost = current load of the machine + the cost of my job performed by that machine
            job_cost_in_m = self.weights.get(machine)
            cost = machine.cost + job_cost_in_m
            if cost < self.cost:
                self.new_machine = machine
                self.cost = cost
        if self.current_machine is None: # first turn, I still have no machine assigned
            self.current_machine = self.new_machine
            self.current_machine.assign_job(self.name, job_cost_in_m)
        elif self.current_machine != self.new_machine:  # I changed my previous machine to a new one
            self.current_machine.deassign_job(self.name)
            self.current_machine = self.new_machine
            self.current_machine.assign_job(self.name, job_cost_in_m)
        # else: I do no change machine, I do nothing



