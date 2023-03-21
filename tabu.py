import pandas as p
import random
import time
import itertools as it
import copy
from time import gmtime, strftime


# preparing data
def change_index(data):
    data.columns.values[0] = 0
    data = data.set_index(0)
    return data


# excel's method Index
def index(data, numbers):
    diff=[]
    for i in range (0, len(data)-1):
        diff.append(data.iloc[numbers[i]-1, numbers[i+1]-1])  # searching diff for neighbour cities
    diff.append(data.iloc[numbers[0]-1, numbers[len(data)-1]-1])  # counts last city with the first
    beginSum = sum(diff)
    return beginSum


# generate list of random numbers from in the range
def random_shuffle(len_data):
    listOfNumbers = list(range(1, len_data+1))
    shuffledNum = listOfNumbers.copy()
    random.shuffle(shuffledNum)
    return shuffledNum


def swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list


# counts profit of switching places of two cities
def bestCombination(data, listOfNumbers, combi):
    profit = []

    for i in range(0, len(combi)-1):
        swapList = copy.deepcopy(listOfNumbers)
        swapList = swapPositions(swapList, combi[i][0]-1, combi[i][1]-1)
        swapSum = index(data, swapList)
        profit.append(swapSum)

    sortedProfit = sorted(profit)
    return sortedProfit, profit


def algorithm(data):
    bestList = []
    maxTabuSize = 5
    tabuList = []
    a = 0

    shuffledNum = random_shuffle(len(data))
    combi = list(it.combinations(shuffledNum, 2))
    t_end = time.time() + 30
    #time.time() < t_end

    while a < 100:
        sortedProfit, profit = bestCombination(data, shuffledNum, combi)

        for i in range(0, len(sortedProfit)-1):
            candidateSum = sortedProfit[i]
            candidate = combi[profit.index(candidateSum)]

            if a == 0:  # set bestSum for first iteration
                bestSum = sortedProfit[0]

            if tabuList.__contains__(candidate):
                continue
            else:
                shuffledNum = swapPositions(shuffledNum, candidate[0] - 1, candidate[1] - 1)
                tabuList.append(candidate)

                if candidateSum <= bestSum:
                    bestSum = candidateSum
                    bestList = copy.deepcopy(shuffledNum)

                if len(tabuList) > maxTabuSize:
                    tabuList.pop(0)

            print(a, "\t", strftime("%H:%M:%S", gmtime()), "\tsum: ", bestSum)
            break
        a += 1
    return bestSum, bestList


# read data
data48 = p.read_excel('Dane_TSP_48.xlsx')
data76 = p.read_excel('Dane_TSP_76.xlsx')
data127 = p.read_excel('Dane_TSP_127.xlsx')

random.seed(100) # ONLY for testing

data = change_index(data48)
bestSum, bestList = algorithm(data)

print("-----------------")
print("bestSum: ", bestSum)
print("bestList: ", bestList)
