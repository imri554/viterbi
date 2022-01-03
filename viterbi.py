import sys
from os import path

pStar = 0
finalAnswer = []

lines = []
inputFile = sys.argv[1]

observationPath = sys.argv[2]

file_object = open(inputFile, "r")
for line in file_object:
    if line is None:
        pStar = 1
    lines.append(line.upper())

# getting all of the data in order
if path.isfile(observationPath):
    observationFile = open(observationPath, "r")
    actualObservations = observationFile.read()
else:
    finalAnswer = None
    p = '{:.4e}'.format(1)
    print(p)
    quit()
if actualObservations == "":
    finalAnswer = None
    p = '{:.4e}'.format(1)
    print(p)
    quit()

numOfHiddenStates = int([x.strip() for x in lines[0].split(',')][0])
numOfObservations = int([x.strip() for x in lines[0].split(',')][1])
hiddenStateNames = [x.strip() for x in lines[1].split(',')]
observationNames = [x.strip() for x in lines[2].split(',')]
initialStateProbabilities = [float(x.strip()) for x in lines[3].split(',')]
transitionMatrix = [x.strip() for x in lines[4].split(';')]
for i in range(0, len(transitionMatrix)):
    dict = {}
    tLine = [x.strip() for x in transitionMatrix[i].split(',')]
    counter = 0
    for each in hiddenStateNames:
        dict[each] = float(tLine[counter])
        counter = counter + 1
    transitionMatrix[i] = dict

# transitions go from rows hidden state to the columns hidden state

observationMatrix = [x.strip() for x in lines[5].split(';')]
for i in range(0, len(observationMatrix)):
    dict = {}
    tLine = [x.strip() for x in observationMatrix[i].split(',')]
    counter = 0
    for each in observationNames:
        dict[each] = float(tLine[counter])
        counter = counter + 1
    observationMatrix[i] = dict

# matrix initialization

scoringMatrix = []
backtrackingMatrix = []
for i in range(0, len(actualObservations)):
    scoringMatrix.append([])
    backtrackingMatrix.append([])

for i in range(0, numOfHiddenStates):
    backtrackingMatrix[0].append(0)
    scoringMatrix[0].append(initialStateProbabilities[i] * observationMatrix[i][actualObservations[0]])

# recurrence

for i in range(1, len(actualObservations)):
    scoringLine = []
    backtrackingLine = []
    counter = 0
    for j in hiddenStateNames:
        scoringMaxOptions = []
        backtrackingArgmaxOptions = {}
        for x in range(0, numOfHiddenStates):
            scoringMaxOptions.append(scoringMatrix[i - 1][x] * transitionMatrix[x][j])
            backtrackingArgmaxOptions[x] = (scoringMatrix[i - 1][x] * transitionMatrix[x][j])
        scoringMatrix[i].append((max(scoringMaxOptions) * observationMatrix[counter][actualObservations[i]]))
        counter = counter + 1

        argmax = max(backtrackingArgmaxOptions, key=lambda x: backtrackingArgmaxOptions[x])
        backtrackingMatrix[i].append(argmax)

# termination
pStar = max(scoringMatrix[len(actualObservations) - 1])
qStar = {}

qStar[len(actualObservations) - 1] = + scoringMatrix[len(scoringMatrix)-1].index(max(scoringMatrix[len(scoringMatrix)-1]))

# backtracking
for t in range(len(actualObservations) - 2, -1, -1):
    qStar[t] = backtrackingMatrix[t+1][qStar[t + 1]]
for t in range(0, len(actualObservations)):
    finalAnswer.append(hiddenStateNames[qStar[t]])

outputString = "".join(finalAnswer)
print(outputString)
print('{:.4e}'.format(pStar))
