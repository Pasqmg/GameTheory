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

    def get_job_cost(self):
        if self.job is not None:
            return self.job.get_cost()

    def set_machines(self, machine_list):
        self.machines = machine_list

    def set_weights(self, weights):
        self.weights = weights

    def get_weight(self, machine_id):
        return self.weights.get(machine_id, -1)

    def update_cost(self):
        if self.current_machine is not None:
            self.cost = self.current_machine.get_cost()
        else:
            self.cost = math.inf

    # select fastest machine as initial machine
    def first_move(self):
        self.current_machine = self.get_fastest()
        # self.current_machine = [m for m in self.weights.keys() if m.speed == min(speed) for speed in [m.speed for m in self.weights.keys()]]
        self.current_machine.assign_job(self.job)

    def get_fastest(self):
        fastest = list(self.weights.keys())[0]
        for m in self.weights.keys():
            if m.speed < fastest.speed:
                fastest = m
        return fastest

    '''
    Checks all machines and chooses to which assign its job to, according to cost
    '''
    def choose_machine(self):
        # Look for a better strategy
        for machine in self.weights.keys():
            # cost = current load of the machine + the cost of my job performed by that machine
            job_cost_in_m = self.weights.get(machine)
            cost = machine.get_cost() + job_cost_in_m
            # if there is a strategy which improves my cost
            if cost < self.cost:
                self.new_machine = machine
                self.cost = cost
        if self.current_machine is None: # first turn, I still have no machine assigned
            self.current_machine = self.new_machine
            self.current_machine.assign_job(self.job)
        elif self.current_machine != self.new_machine:  # I changed my previous machine to a new one
            self.current_machine.deassign_job(self.job)
            self.current_machine = self.new_machine
            self.current_machine.assign_job(self.job)
        # else: I do no change machine, I do nothing

    '''
    Checks all machines and chooses to which assign its job to, according to cost
    '''

    def choose_machine_2(self):
        # cost_before = self.cost
        # updated_cost = self.current_machine.get_cost()
        # Look for a better strategy
        for machine in self.weights.keys():
            # cost = current load of the machine + the cost of my job performed by that machine
            job_cost_in_m = self.weights.get(machine)
            cost = machine.get_cost() + job_cost_in_m
            # if there is a strategy which improves my cost
            if cost < self.cost:
                self.new_machine = machine
                self.cost = cost
        if self.current_machine != self.new_machine and self.new_machine is not None:  # I changed my previous machine to a new one
            self.current_machine.deassign_job(self.job)
            self.current_machine = self.new_machine
            self.current_machine.assign_job(self.job)



