"""
Class Game:
    - Creates a game with the indicated number of players and machines
    - The setup_game() function must be modify to define the game elements and costs
    - The function play() reproduces the Best-Response behaviour
        - The Best-Response strategy is chosen by function choose_machine() of the Player class
"""
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import math

from loguru import logger
from load_balancing_game.Machine import Machine
from load_balancing_game.Player import Player
from load_balancing_game.Job import Job

data_dic = {}
num_players = 5
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
        return 3 * n

    machines[1].compute_custom_cost = compute_custom_cost

    machines.append(Machine("slow_machine", 1))

    def compute_custom_cost(n):
        return 5 * (n - 1) + 4

    machines[2].compute_custom_cost = compute_custom_cost

    # Gives each player a job and precalculates the cost of such job in every machine, storing it in weights dict.
    for p in range(num_players):
        weights = {}
        players[p].set_job(Job(players[p].name, 1))
        for m in range(num_machines):
            if machines[m].compute_custom_cost is None:
                weights[machines[m]] = machines[m].get_speed() * players[p].get_job_cost()
            else:  # we are using custom costs
                players[p].machines.append(machines[m])
        players[p].set_weights(weights)

    logger.info("_________________________________________________________________________")
    logger.info("\t\t\t\t\t\t\tGame setup")
    logger.info("-------------------------------------------------------------------------")
    for p in players:
        logger.debug("Player {} has job {}".format(p.get_name(), p.job.print()))

def show_machine_function():
    x = np.linspace(0,6,100)
    y = pow(2,x)
    w = 3*x
    z = 5 * (x - 1) + 4

    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    plt.xlabel('Amount of jobs')
    plt.ylabel('Machine cost')

    # plot the function
    plt.plot(x, y, 'c', linestyle='-', label="Fast machine", linewidth=2)
    plt.plot(x, w, 'm', linestyle='-', label = "Medium machine", linewidth=2)
    plt.plot(x, z, 'y', linestyle='-', label = "Slow machine", linewidth=2)

    # show the plot
    chartBox = ax.get_position()
    ax.set_position([chartBox.x0, chartBox.y0, chartBox.width * 0.6, chartBox.height])
    ax.legend(loc='upper center', bbox_to_anchor=(0.3, 1), shadow=True, ncol=1)
    # ax.legend()
    plt.show()

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


def save_game_data(game_num, players, costs):

    data_dic[game_num] = (players, costs)

def plot_data(data_dic):
    # libraries
    import numpy as np
    import pandas as pd

    players_dic = {}

    players_dic['x'] = []
    for game in data_dic:
        tuple = data_dic[game]
        players = tuple[0]
        costs = tuple[1]
        players_dic['x'].append(len(players))
        for p in range(len(players)):
            list_of_costs = players_dic.get(players[p])
            if list_of_costs is None:
                list_of_costs = []
            list_of_costs.append(costs[p])
            players_dic[players[p]] = list_of_costs

    print(players_dic)
    for game in data_dic:
        tuple = data_dic[game]
        players = tuple[0]
        costs = tuple[1]
        for p in range(len(players)):
            list_of_costs = players_dic.get(players[p])
            while len(list_of_costs) < num_players-1:
                list_of_costs.insert(0, 0)
            players_dic[players[p]] = list_of_costs

    # Data
    # df = pd.DataFrame({'x': range(1, len(data_dic)), 'y1': np.random.randn(10), 'y2': np.random.randn(10) + range(1, 11),
    #                    'y3': np.random.randn(10) + range(11, 21)})

    #df = pd.DataFrame.from_dict(players_dic)
    x = players_dic.get('x')
    players_dic.pop('x')
    xi = list(range(len(x)))
    print(x, xi)
    # multiple line plot
    for key in players_dic.keys():
        #plt.plot(players_dic.get('x')[0:len(players_dic.get(key))], players_dic.get(key), label=key)
        plt.plot(xi, players_dic.get(key), marker='', label=key)
        #plt.plot(players_dic.get('x'), key, data=players_dic.get(key), color=np.random.rand(3,))
    plt.xlabel('Amount of players')
    plt.ylabel('Cost')
    plt.xticks(xi, x)
    plt.title('compare')
    plt.legend()
    plt.show()
    # plt.plot('x', 'player_1', data=df, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
    # plt.plot('x', 'player_2', data=df, marker='', color='olive', linewidth=2)
    # plt.plot('x', 'y3', data=df, marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")
    # plt.legend()

costs_dic = {}
machine_dic = {}
x, minimums, maximums, averages = [], [], [], []
game = 0
# for num_players in [10, 10, 10, 10, 10] :#range(2,101):
#     game += 1
#     logger.info("_________________________________________________________________________")
#     logger.info("\t\t\t\t\t\t\tGame {}".format(game))
#     logger.info("-------------------------------------------------------------------------")
#     logger.info("-------------------------------------------------------------------------")
#     setup_game(num_players, num_machines)
#
#     if num_players == 2:
#         show_machine_function()
#     # random order among players
#     # random.shuffle(players)
#     play()
#
#     names = [p.name for p in players]
#     costs = [p.cost for p in players]
#
#     # cost data
#     x.append(len(players))
#     min_c = min(costs)
#     max_c = max(costs)
#     avg_c = sum(costs)/len(costs)
#
#     minimums.append(min_c)
#     maximums.append(max_c)
#     averages.append(avg_c)
#     costs_dic[game] = [min_c, avg_c, max_c]
#
#     # jobs data
#     if num_players == 2:
#         for m in machines:
#             machine_dic[m.id] = []
#
#     #for m in machines:
#         #machine_dic[m.id].append(len(m.assigned_jobs))
#
#     save_game_data(game, names, costs)
#
#     # fig = plt.figure(u'Gráfica de barras')  # Figure
#     # ax = fig.add_subplot(111)  # Axes
#     # xx = range(len(costs))
#     # ax.bar(xx, costs, width=0.6, align='center')
#     # ax.set_xticks(xx)
#     # ax.set_xticklabels(names)
#     # plt.show()
#     logger.info("                                                                         ")
#     players = []
#     machines = []
#
# xi = list(range(len(x)))
#
# plt.plot(xi, maximums, color='r', label="Max. cost")
# plt.plot(xi, averages, color='b', label="Avg. cost")
# plt.plot(xi, minimums, color='g', label="Min. cost")
#
#
# plt.xlabel('Amount of players')
# plt.ylabel('Cost')
# plt.xticks(xi, x)
# plt.title('Player increase vs Cost increase')
# plt.legend()
# plt.show()
#
# # jobs plot
#
# plt.plot(xi, machine_dic.get('fast_machine'), color='c', label="Fast machine", linewidth=2)
# plt.plot(xi, machine_dic.get('medium_machine'), color='m', label="Medium machine", linewidth=2)
# plt.plot(xi, machine_dic.get('slow_machine'), color='y', label="Slow machine", linewidth=2)
#
# plt.xlabel('Amount of players')
# plt.ylabel('Jobs in machine')
# plt.xticks(xi, x)
# plt.title('Player increase vs Job distribution')
# plt.legend()
# plt.show()

list_averages_no_shuffle = []
list_averages_shuffle = []
for num_players in [5, 10, 15]:
    players_dic = {}
    max_avg_cost = -1
    setup_game(num_players, num_machines)
    random.shuffle(players)
    play()
    # avg cost data
    for p in players:
        list_of_costs = players_dic.get(p.name)
        if list_of_costs is None:
            list_of_costs = []
        list_of_costs.append(p.cost)
        players_dic[p.name] = list_of_costs

    players = []
    machines = []

    # player avg cost plot
    averag_list = []
    keys = list(players_dic.keys())
    fig = plt.figure(u'Gráfica de barras')  # Figure
    ax = fig.add_subplot(111)  # Axes
    xx = [n for n in range(0, num_players + 1)]
    for i in range(len(keys)):
        player = keys[i]
        costs = players_dic.get(player)
        avg_cost = sum(costs) / len(costs)
        averag_list.append(avg_cost)
        if avg_cost > max_avg_cost:
            max_avg_cost = avg_cost
        ax.bar(xx[i + 1], avg_cost, width=0.6, align='center', color="blue")
        # xx = range(len(costs))
        # ax.bar(xx, costs, width=0.6, align='center')
    ax.set_xticks(xx)
    ax.set_xticklabels(xx)
    plt.xlabel('Player')
    plt.ylabel('Cost')
    plt.title('Player average cost')
    ylimits = ax.get_ylim()
    plt.show()
    list_averages_no_shuffle.append((num_players, sum(averag_list)/len(averag_list)))

    players_dic = {}
    averag_list = []
    for games in range(100):

        setup_game(num_players, num_machines)
        random.shuffle(players)
        play()
        # avg cost data
        for p in players:
            list_of_costs = players_dic.get(p.name)
            if list_of_costs is None:
                list_of_costs = []
            list_of_costs.append(p.cost)
            players_dic[p.name] = list_of_costs


        players = []
        machines = []

    # player avg cost plot
    keys = list(players_dic.keys())
    fig = plt.figure(u'Gráfica de barras')  # Figure
    ax = fig.add_subplot(111)  # Axes
    xx = [n for n in range(0,num_players+1)]
    #yy = [n for n in range(0, math.ceil(max_avg_cost+1))]
    for i in range(len(keys)):
        player = keys[i]
        costs = players_dic.get(player)
        avg_cost = sum(costs)/len(costs)
        averag_list.append(avg_cost)
        ax.bar(xx[i+1], avg_cost, width=0.6, align='center', color="blue")
        # xx = range(len(costs))
        # ax.bar(xx, costs, width=0.6, align='center')
    ax.set_xticks(xx)
    ax.set_xticklabels(xx)
    ax.set_ylim(ylimits)
    #plt.yticks(yy, yy)
    plt.xlabel('Player')
    plt.ylabel('Cost')
    plt.title('Player average cost (shuffling)')
    plt.show()
    list_averages_shuffle.append((num_players, sum(averag_list)/len(averag_list)))
print(list_averages_no_shuffle)
print(list_averages_shuffle)

