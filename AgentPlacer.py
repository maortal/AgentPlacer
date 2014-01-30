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

#key = '1'
#while key != '0\n':
if len(sys.argv) > 4:
    chosenMap = int(sys.argv[1])
    percentageOfAgents = float(sys.argv[2])
    percentageOfNonCompliant = float(sys.argv[3])
    iteration = int(sys.argv[4])
else:
    while True:
        chosenMap = int(raw_input("Enter map ID: "))
        if (chosenMap <= index) & (chosenMap > 0):
            break
    percentageOfAgents = float(raw_input("Enter Percentage of agents to cover the map: "))
    percentageOfNonCompliant = float(raw_input("Enter Percentage of non compliant agents: "))
    iteration = int(raw_input("Enter number of iterations: "))

numberOfAgents = int(availableMaps[chosenMap]['States'] * (percentageOfAgents / 100.0))
numberOfNonComp = int(numberOfAgents * (percentageOfNonCompliant / 100.0))
filename = "{0}-T_{1}-NC_{2}.txt".format(str(availableMaps[chosenMap]['Name']).split('.')[0], str(numberOfAgents),
                                         str(int(numberOfNonComp)))

agentsIndexs = []
Nagents = numberOfAgents
placeagents = reduce(list.__add__, (list(mi) for mi in availableMaps[chosenMap]['Map']))
while Nagents > 0:
    ind = random.randint(0, len(placeagents) - 1)
    while placeagents[ind] != '.':
        ind = random.randint(0, len(placeagents) - 1)
    agentsIndexs.append(ind)
    placeagents[ind] = 'c'
    Nagents -= 1


while iteration > 0:
    placeagentsTemp= list(placeagents)
    tmpagentsIdx = list(agentsIndexs)
    NnonCagents = numberOfNonComp
    from random import choice
    while NnonCagents > 0:
        placeNonCompliant = choice(tmpagentsIdx)
        tmpagentsIdx.remove(placeNonCompliant)
        placeagentsTemp[placeNonCompliant] = 'n'
        NnonCagents-=1

    savepath = "ready\\" + os.path.splitext(availableMaps[chosenMap]['Name'])[0] + "\\"
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    with open(savepath + os.path.splitext(filename)[0] + "-I" + str(iteration) + os.path.splitext(filename)[1], 'w') as file:
        for item in placeagentsTemp:
            file.write("%s" % item)
    iteration -= 1
   # print("Press 0 to quit or any key to continue")
   # key = str(sys.stdin.readline())
   # key ="0\n"