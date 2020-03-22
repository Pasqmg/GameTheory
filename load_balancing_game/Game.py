from loguru import logger
from load_balancing_game.Machine import Machine
from load_balancing_game.Player import Player

num_players = 4
num_machines = 4
players = []
machines = []

# print final state
def print_game():
    print("END of Game\n---------------------------")
    for p in players:
        print("Player", p.name, "Machine", p.current_machine.id, "cost", p.cost)
    for m in machines:
        print("Machine", m.id, "cost", m.cost, "has assigned", m.assigned_jobs)

# game setup
for i in range(num_players):
    players.append(Player("player_"+str(i+1)))

for j in range(num_machines):
    machines.append(Machine(j+1))

for p in players:
    weights = {}
    for m in machines:
        weights[m] = 5
    p.set_weights(weights)

# print game
print("Game status\n---------------------------")
for p in players:
    print("Player", p.name, "\n")
    for m in machines:
        w = p.get_weight(m)
        print("Machine", m.id, "cost:", w)
    print("\n")

# random order among players
#random.shuffle(players)

# turn
# 1. Machines compute their current cost
# 2. Players decide to which machine they assign their job
end = False
turn = 0
while not end:
    # One turn of the game: each player chooses a machine, one after another
    turn += 1
    logger.info("Game turn {}".format(turn))
    # Update machine costs
    for m in machines: m.compute_cost()
    # Keep track of changes in player's strategies
    change = []
    # for each player in the game
    for p in players:

        cost_before = p.cost
        p.choose_machine()
        cost_after = p.cost
        if cost_before != cost_after:
            change.append(True)
        else:
            change.append(False)
        # update costs
        for m in machines: m.compute_cost()
    if not any(change):
        end = True
    print_game()



print("END of Game\n---------------------------")
for p in players:
    print("Player", p.name, "Machine", p.current_machine.id, "cost", p.cost)
for m in machines:
    print("Machine", m.id, "cost", m.cost, "has assigned", m.assigned_jobs)


