
class Machine:

    def __init__(self, id):
        self.id = id
        self.assigned_jobs = []
        self.cost = 0
        self.free_time = -1
        self.end_time = -1

    def compute_cost(self):
        if self.assigned_jobs:
            cost = 0
            for player,job in self.assigned_jobs:
                cost += job
            self.cost = cost

    def assign_job(self, player_name, cost):
        self.assigned_jobs.append((player_name, cost))

    def deassign_job(self, delete_player):
        self.assigned_jobs = [(player_name, cost) for player_name, cost in self.assigned_jobs if player_name != delete_player]