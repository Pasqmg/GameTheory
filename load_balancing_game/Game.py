"""
Class Game:
    - Creates a game with the indicated number of players and machines
    - The setup_game() function must be modify to define the game elements and costs
    - The function play() reproduces the Best-Response behaviour
        - The Best-Response strategy is chosen by function choose_machine() of the Player class
"""

import random

from loguru import logger
from load_balancing_game.Machine import Machine
from load_balancing_game.Player import Player
from load_balancing_game.Job import Job

num_players = 6
num_machines = 3
players = []
machines = []


# NOT IN USE ANYMORE
# weight_matrix = [  # m1, m2, m3, m4
#     [20, 10, 1, 5],  # player_1
#     [20, 10, 1, 5],  # player_2
#     [20, 10, 5, 5],  # player_3
#     [1, 2, 3, 6]  # player_4
# ]


# print final state
def print_game():
    for p in players:
        print("Player", p.name, "Machine", p.current_machine.id, "cost", p.cost)
    for m in machines:
        print("Machine", m.id, "cost", m.cost, "has assigned", m.assigned_jobs)


"""
    - Creates num_players players
    - The user must manually create EXACTLY num_machines machines, defining its name and speed (multiplier)
    - Currently all players have one job with the same base cost (10)
"""
def setup_game(num_players, num_machines):
    # game setup
    for i in range(num_players):
        players.append(Player("player_" + str(i + 1)))

    machines.append(Machine("fast_machine", 0.3))
    def compute_custom_cost(n):
        return pow(2, n)
    machines[0].compute_custom_cost = compute_custom_cost

    machines.append(Machine("medium_machine", 0.5))
    def compute_custom_cost(n):
        return 3*n
    machines[1].compute_custom_cost = compute_custom_cost

    machines.append(Machine("slow_machine", 1))
    def compute_custom_cost(n):
        return 4*(n-1)+4
    machines[2].compute_custom_cost = compute_custom_cost


    # Gives each player a job and precalculates the cost of such job in every machine, storing it in weights dict.
    for p in range(num_players):
        weights = {}
        players[p].set_job(Job(players[p].name, 1))
        for m in range(num_machines):
            if machines[m].compute_custom_cost is None:
                weights[machines[m]] = machines[m].get_speed() * players[p].get_job_cost()
            else : # we are using custom costs
                players[p].machines.append(machines[m])
        players[p].set_weights(weights)

    logger.info("_________________________________________________________________________")
    logger.info("\t\t\t\t\t\t\tGame setup")
    logger.info("-------------------------------------------------------------------------")
    for p in players:
        logger.info("Player {} has job {}".format(p.get_name(), p.job.print()))


def play():
    end = False
    turn = 0
    while not end:
        # One turn of the game: each player chooses a machine, one after another
        turn += 1
        logger.info("_________________________________________________________________________")
        logger.info("\t\t\t\t\t\t\tGame turn {}".format(turn))
        logger.info("-------------------------------------------------------------------------")
        # Keep track of changes in player's strategies
        change = []
        # for each player in the game
        for p in players:
            # update cost of the current player
            p.update_cost()
            cost_before, machine_before = p.cost, p.current_machine
            # look for a better strategy
            p.choose_machine()
            cost_after, machine_after = p.cost, p.current_machine
            if cost_before != cost_after:
                change.append(True)
                if turn == 1:
                    logger.info(
                        "Player {} chose machine {} as their first machine, reducing their cost from {} to {}".format(
                            p.name, machine_after.id, cost_before, cost_after))
                else:
                    logger.info(
                        "Player {} changed from machine {} to machine {} reducing their cost from {} to {}".format(
                            p.name, machine_before.id, machine_after.id, cost_before, cost_after))
            else:
                change.append(False)
                logger.info("Player {} did not change their machine".format(p.name))
            # update players costs for next turn
            p.update_cost()
        if not any(change):
            end = True

    logger.info("_________________________________________________________________________")
    logger.info("\t\t\t\t\t\t\tEND of Game")
    logger.info("-------------------------------------------------------------------------")
    for p in players:
        logger.info("Player {} has {} with a cost of {}".format(p.name, p.current_machine.id, p.cost))
    for m in machines:
        logger.info("Machine {} with cost {} has assigned {}".format(m.id, m.cost, m.print_jobs()))


setup_game(num_players, num_machines)
# random order among players
random.shuffle(players)
play()

import matplotlib.pyplot as plt

fig = plt.figure(u'Gráfica de barras')  # Figure
ax = fig.add_subplot(111)  # Axes

names = [p.name for p in players]
costs = [p.cost for p in players]
xx = range(len(costs))

ax.bar(xx, costs, width=0.6, align='center')
ax.set_xticks(xx)
ax.set_xticklabels(names)

plt.show()
