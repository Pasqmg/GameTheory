"""
Class Machine:
    - A machine will have a speed and a series of jobs assigned to it
    - Depending on the speed, the time consumed to perform those jobs will change
    - Such time defines the cost of the machine, which is also the cost for the player that assigned its job to it
"""


class Machine:

    def __init__(self, id, speed):
        self.id = id
        self.assigned_jobs = []
        self.speed = speed
        self.cost = 0
        self.free_time = -1
        self.end_time = -1
        self.compute_custom_cost = None

    # Updates a machine cost every time it gets a job assigned or deassigned
    def compute_cost(self):
        if self.compute_custom_cost is None:
            if self.assigned_jobs:
                cost = 0
                for job in self.assigned_jobs:
                    cost += self.speed * job.get_cost()
                self.cost = cost
        else:
            self.cost = self.compute_custom_cost(len(self.assigned_jobs))

    def get_cost_of_adding_one_job(self):
        return self.compute_custom_cost(len(self.assigned_jobs)+1)

    def get_cost(self):
        return self.cost

    def get_speed(self):
        return self.speed

    def assign_job(self, job):
        self.assigned_jobs.append((job))
        self.compute_cost()

    def deassign_job(self, delete_job):
        self.assigned_jobs = [job for job in self.assigned_jobs if job.owner != delete_job.owner]
        self.compute_cost()

    def print_jobs(self):
        l = []
        for job in self.assigned_jobs:
            s = job.print()
            l.append(s)
        return l
