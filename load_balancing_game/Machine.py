
class Machine:

    def __init__(self, id, speed):
        self.id = id
        self.assigned_jobs = []
        self.speed = speed
        self.cost = 0
        self.free_time = -1
        self.end_time = -1

    def compute_cost(self):
        if self.assigned_jobs:
            cost = 0
            for job in self.assigned_jobs:
                cost += self.speed * job.get_cost()
            self.cost = cost

    def get_cost(self):
        return self.cost

    def assign_job(self, job):
        self.assigned_jobs.append((job))
        self.compute_cost()

    def deassign_job(self, delete_job):
        self.assigned_jobs = [job for job in self.assigned_jobs if job.owner != delete_job.owner]
        # self.assigned_jobs = [(player_name, job) for player_name, job in self.assigned_jobs if player_name != delete_player]
        self.compute_cost()

    def print_jobs(self):
        l = []
        for job in self.assigned_jobs:
            s = job.print() #"<"+str(job.owner), str(job.get_cost())+">"
            l.append(s)
        return l