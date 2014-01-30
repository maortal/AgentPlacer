__author__ = 'maor'
import os
import random
import sys

availableMaps = {}


def NumberofStates(filename):
    with open(filename) as file:
        x = file.readlines()
    sum = 0
    for line in x:
        sum += line.count(".")
    return {'States': sum, 'Map': x}


index = 1
print("Listing Available Maps:\n")
for f in os.listdir('.'):
    if f.endswith('.txt'):
        availableMaps[index] = {'Name': f}
        availableMaps[index].update(NumberofStates(f))
        print(str(index) + ". " + f + "\t\tStates: " + str(availableMaps[index]['States']))
        index += 1

key = '1'
while key != '0\n':
    while True:
        chosenMap = int(raw_input("Enter map ID: "))
        if (chosenMap <= index) & (chosenMap > 0):
            break
    percentageOfAgents = int(raw_input("Enter Percentage of agents to cover the map: "))
    numberOfAgents = availableMaps[chosenMap]['States'] * (percentageOfAgents / 100.0)
    percentageOfNonCompliant = int(raw_input("Enter Percentage of non compliant agents: "))
    numberOfNonComp = numberOfAgents * (percentageOfAgents / 100.0)
    filename = "{0}-T_{1}-NC_{2}.txt".format(str(availableMaps[chosenMap]['Name']).split('.')[0], str(numberOfAgents),
                                             str(int(numberOfNonComp)))
    iteration = int(raw_input("Enter number of iterations: "))
    while iteration > 0:
        Nagents = numberOfAgents
        NnonCagents = numberOfNonComp
        placeagents = reduce(list.__add__, (list(mi) for mi in availableMaps[chosenMap]['Map']))
        while Nagents > 0:
            ind = random.randint(0, len(placeagents)-1)
            while placeagents[ind] != '.':
                ind = random.randint(0, len(placeagents)-1)
            if NnonCagents > 0:
                NnonCagents -= 1
                placeagents[ind] = 'n'
            else:
                placeagents[ind] = 'c'
            Nagents -= 1
        if not os.path.exists('ready'):
            os.makedirs('ready')
        with open("ready\\" + str(iteration) + "-" + filename, 'w') as file:
            for item in placeagents:
                file.write("%s" % item)
        iteration -= 1
    print("Press 0 to quit or any key to continue")
    key = str(sys.stdin.readline())