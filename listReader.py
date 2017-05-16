#Written by Daniel C. Here we are taking in a file and reading the contents to thefile and storing them.

import string

def generateTrainingLists(fileName):
    file = open(fileName, "r")
    lineList = file.readlines()
    lineList = list(map(standardize, lineList))
    trainingLists = []
    begin = 0
    end = 0
    for i in range(0, len(lineList)):
        if (lineList[i] == '' or i == len(lineList) - 1):
            end = i
            trainingLists.append(map(standardize, lineList[begin:end]))
            begin = end + 1
            
    return(trainingLists)

def standardize(msg):
    line = msg.lower()
    line = line.translate(None, "?.;!*&%@#^$*()+=<>|-\"")
    line = " ".join(line.split())
    return line