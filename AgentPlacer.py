import re
import os
import sys
import math
import random

__author__ = 'maor'

availableMaps = {}


class Exit:
    def __init__(self, x, y, p):
        self.X = x
        self.Y = y
        try:
            self.Priority = float(p)
        except ValueError:
            self.Priority = 1


class State:
    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.Prob = 0
        self.NormalizedProb = 0

class Map:
    def __init__(self, filename):
        with open(filename) as file:
            x = file.readlines()
        self.FileName = filename
        self.RawMap = []
        self.Height = int(x[0].split()[0])
        self.Width = int(x[0].split()[1])+1 #+1 for end line
        listPrio = []
        for line in x[1:]:
            for m in re.finditer('>(?P<prio>\d*(\.\d+)?)', line):
                listPrio.append(m.group('prio'))
            spline = re.sub('\d*(\.\d+)?', '', line)
            self.RawMap.append(spline)
        self.sumAllstatesProb = 0
        self.numOfStates = 0
        self.Exits = []
        self.States = []
        for y, line in enumerate(self.RawMap):
            for m in re.finditer('>', line):
                self.Exits.append(Exit(m.start(), y, listPrio.pop(0)))
            for d in re.finditer('\.', line):
                self.States.append(State(d.start(), y))
                self.numOfStates += 1
        self.calcStateProbs()

    def calcStateProbs(self):
        self.sumAllstatesProb = 0
        for state in self.States:
            statesum = 0
            for exit in self.Exits:
                d_i = abs(state.X - exit.X) + abs(state.Y - exit.Y) #manhattan distance
                statesum += (d_i * (-exit.Priority))
            state.Prob = math.exp(statesum)
            self.sumAllstatesProb += state.Prob

        #normalize probs if needed in future...
        for state in self.States:
            state.NormalizedProb = state.Prob / self.sumAllstatesProb

    def placeAgents(self, numOfAgents):
        placeAgents = list(self.States)
        returnIDX = []
        tmpsum = self.sumAllstatesProb
        while numOfAgents > 0:
            r = random.uniform(0, tmpsum)
            upto = 0
            for p in placeAgents:
                upto += p.Prob
                if upto > r:
                    placeAgents.remove(p)
                    returnIDX.append(p.X + (p.Y * self.Width))
                    tmpsum -= p.Prob
                    numOfAgents -= 1
                    break
        return returnIDX


if __name__ == "__main__":
    index = 1
    print("Listing Available Maps:\n")
    for f in os.listdir('.'):
        if f.endswith('.txt'):
            availableMaps[index] = Map(f)
            print("%s. %s \t [States: %s Exits: %s]" % (
                index, f, availableMaps[index].numOfStates, len(availableMaps[index].Exits)))
            index += 1

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

    numberOfAgents = int(availableMaps[chosenMap].numOfStates * (percentageOfAgents / 100.0))
    numberOfNonComp = int(numberOfAgents * (percentageOfNonCompliant / 100.0))
    filename = "{0}-T_{1}-NC_{2}.txt".format(str(availableMaps[chosenMap].FileName).split('.')[0], str(numberOfAgents),
                                             str(int(numberOfNonComp)))

    agentsIndexs = []
    Nagents = numberOfAgents
    placeagents = reduce(list.__add__, (list(mi) for mi in availableMaps[chosenMap].RawMap))
    agentsIndexs = availableMaps[chosenMap].placeAgents(numberOfAgents)

    for pos in agentsIndexs:
        placeagents[pos] = 'c'

    #these iterations are for selection non compliant agents
    while iteration > 0:
        placeagentsTemp = list(placeagents)
        tmpagentsIdx = list(agentsIndexs)
        NnonCagents = numberOfNonComp

        while NnonCagents > 0:
            placeNonCompliant = random.choice(tmpagentsIdx)
            tmpagentsIdx.remove(placeNonCompliant)
            placeagentsTemp[placeNonCompliant] = 'n'
            NnonCagents -= 1

        savepath = "ready\\" + os.path.splitext(availableMaps[chosenMap].FileName)[0] + "\\"
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        with open(savepath + os.path.splitext(filename)[0] + "-I" + str(iteration) + os.path.splitext(filename)[1],
                  'w') as file:
            file.write("%s %s\n" % (availableMaps[chosenMap].Height, availableMaps[chosenMap].Width-1))
            for item in placeagentsTemp:
                file.write("%s" % item)
        iteration -= 1
        # print("Press 0 to quit or any key to continue")
        # key = str(sys.stdin.readline())
        # key ="0\n"
