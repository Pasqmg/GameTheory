import random

from loguru import logger
from load_balancing_game.Machine import Machine
from load_balancing_game.Player import Player
from load_balancing_game.Job import Job

num_players = 5
num_machines = 3
players = []
machines = []

weight_matrix = [  # m1, m2, m3, m4
    [20, 10, 1, 5],  # player_1
    [20, 10, 1, 5],  # player_2
    [20, 10, 5, 5],  # player_3
    [1, 2, 3, 6]  # player_4
]


# print final state
def print_game():
    for p in players:
        print("Player", p.name, "Machine", p.current_machine.id, "cost", p.cost)
    for m in machines:
        print("Machine", m.id, "cost", m.cost, "has assigned", m.assigned_jobs)


"""
Player and machine creation. Assigns weigths to each player's job according to the weight matrix
"""


def setup_game(num_players, num_machines):
    # game setup
    for i in range(num_players):
        players.append(Player("player_" + str(i + 1)))

    machines.append(Machine("fast_machine", 0.3))
    machines.append(Machine("medium_machine", 0.5))
    machines.append(Machine("slow_machine", 1))

    for p in range(num_players):
        weights = {}
        players[p].set_job(Job(players[p].name, 10))
        for m in range(num_machines):
            weights[machines[m]] = machines[m].speed * players[p].get_job_cost()
        players[p].set_weights(weights)
        # print(players[p].name)
        # for m in players[p].weights:
        #     print(m.id, ':', players[p].weights[m])

    logger.info("_________________________________________________________________________")
    logger.info("\t\t\t\t\t\t\tGame setup")
    logger.info("-------------------------------------------------------------------------")
    for p in players:
        logger.info("Player {} has job {}".format(p.name, p.job.print()))


# print game
'''
print("Game status\n---------------------------")
for p in range(num_players):
    print("Player", p.name, "\n")
    for m in range(machines):
        w = p.get_weight(m)
        print("Machine", m.id, "cost:", w)
    print("\n")
'''


def play():
    # turn
    # 1. Machines compute their current cost
    # 2. Players decide to which machine they assign their job
    """
    for p in players:
        p.first_move()
        p.update_cost()
    """
    end = False
    turn = 0
    while not end:
        # One turn of the game: each player chooses a machine, one after another
        turn += 1
        logger.info("_________________________________________________________________________")
        logger.info("\t\t\t\t\t\t\tGame turn {}".format(turn))
        logger.info("-------------------------------------------------------------------------")
        # Update machine costs
        # for m in machines: m.compute_cost()
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
            # update costs
            # for m in machines: m.compute_cost()
            p.update_cost()
        if not any(change):
            end = True
        # print_game()

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
