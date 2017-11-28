import math
import operator
import sqlite3
import random
import sys
import progressbar
import time
import datetime

con = sqlite3.connect('./database/db')
cur = con.cursor()


def loadDataset(split, trainingSet=[], testSet=[]):
    with con:
        cur.execute('SELECT * FROM cases')
        dataset2 = list(cur.fetchall())
        dataset = []
        for x in dataset2:
            dataset.append(list(x[1:]))
        cur.execute('SELECT * FROM preferences')
        pref = list(cur.fetchall())
        pref2 = []
        for el in pref:
            pref2.append(list(el[2:]))
        pref = [ii for n, ii in enumerate(pref2) if ii not in pref2[:n]]
        prefer, users = {}, {}
        for el in pref:
            users_temp = {el[0]: float(el[1] / 2)}
            prefer_temp = {el[0]: dict(Energy=float(el[2] / 5), Entertainment=float(el[3] / 5), Food=float(el[4] / 5),
                                       Health=float(el[5] / 5), Security=float(el[6] / 5), Work=float(el[7] / 5))}
            prefer.update(prefer_temp)
            users.update(users_temp)
        for x in range(len(dataset)):
            dataset[x][1] = prefer[dataset[x][0]][dataset[x][1]]
            dataset[x][3] = prefer[dataset[x][2]][dataset[x][3]]
            dataset[x][0] = users[dataset[x][0]]
            dataset[x][2] = users[dataset[x][2]]
            if random.random() < split:
                trainingSet.append(dataset[x])
            else:
                testSet.append(dataset[x])


def euclideanDistance(instance1, instance2, length, weights):
    distance = 0
    for x in range(length):
        distance += weights[x] * pow((instance1[x] - instance2[x]), 2)
    try:
        return math.sqrt(distance)
    except ValueError:
        print(distance)
        print(weights)
        sys.exit(0)


def getNeighbors(trainingSet, testInstance, k, weights):
    distances = []
    length = len(testInstance) - 1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x], length, weights)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    # print("Distances are:")
    # print(distances)
    neighbors = []
    for x in range(len(distances)):
        if distances[x][1] <= k:
            neighbors.append(distances[x][0])
    # print('neighbors are:')
    # print(neighbors)
    if neighbors != None:
        neighbors.append(distances[0][0])
    return neighbors


def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
    # print(sortedVotes)
    # print("Value is:")
    # print(sortedVotes[0][0])
    return sortedVotes[0][0]


def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet) - 1):
        if testSet[x][-1] == predictions[x]:
            correct += 1
    return (correct / float(len(testSet))) * 100.0


def specy(TrescholdValue, weights):
    # prepare data
    trainingSet = []
    testSet = []
    split = 0.67
    loadDataset(split, trainingSet, testSet)
    # print('Train set: ' + repr(len(trainingSet)))
    # print('Test set: ' + repr(len(testSet)))
    # generate predictions
    predictions = []
    for x in range(len(testSet)):
        neighbors = getNeighbors(trainingSet, testSet[x], TrescholdValue, weights)
        result = getResponse(neighbors)
        predictions.append(result)
        # print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
    accuracy = getAccuracy(testSet, predictions)
    # print('Accuracy: ' + repr(accuracy) + '%')
    return accuracy


weights = [float(1), float(1), float(1), float(1), float(1), float(1)]
TresholdValue = 0.2
start_time = time.time()
king = {"Epoch": 0, "Genome": weights, "Accuracy": float(specy(TresholdValue, weights))}
speed = time.time() - start_time
mutations = []
mutationstypes = []

listLength = 6
for x in range(0, 2 ** listLength):
    mutationstypes.append(list(bin(x)[2:].zfill(listLength)))
    for z in range(len(mutationstypes)):
        mut = [0, 0, 0, 0, 0, 0]
        mut2 = [0, 0, 0, 0, 0, 0]
        for j in range(6):
            mut[j] = int(mutationstypes[z][j])
            mut2[j] = -1 * int(mutationstypes[z][j])
            # print(j)
        mutations.append(mut)
        mutations.append(mut2)
mutations = [list(x) for x in set(tuple(x) for x in mutations)]
# print(len(mutations))
while 1:
    Epos = int(input("Write number of epochs: "))
    Deep = int(input("Write deepness: "))
    print("Number of epochs is " + str(Epos))
    print("Deepness of the analysis is " + str(Deep))
    execution_time = 1.1 * speed * Epos * Deep * int(len(mutations))
    print("Estimated execution time is " + str(datetime.timedelta(seconds=int(execution_time))))
    print("Estimated execution time for one epoch is " + str(datetime.timedelta(seconds=int(execution_time / 100000))))
    ans = int(input("Is it okay? (type 1 for yes, type 0 for no)"))
    if ans == 1:
        break
# print("Estimated execution time is " + str(datetime.timedelta(seconds=int(execution_time))))
# print("Estimated execution time for one epoch is " + str(datetime.timedelta(seconds=int(execution_time/100000))))
print("=======================================================================")
print("Starting evolutional algorithm: ")
bb = 0
print("=======================================================================")
print()
print()
print("Epoch num is 0")
print("- - - - - - - - - - - - -")
print("King is:")
print(king)
bar = progressbar.ProgressBar().start()
bar.update(bb)
genome = weights
for epoha in range(Epos):
    organism = []
    for x in range(Deep):
        for k in range(len(mutations)):
            new_weight = [float(i) * pow(10.0, -x) for i in mutations[k]]
            genome = [abs(float((x + y))) for x, y in zip(genome, new_weight)]
            # print(genome)
            organism.append({"Epoch": epoha, "Genome": genome, "Accuracy": float(specy(TresholdValue, genome))})
            # print({"Epoch": epoha, "Genome": genome, "Accuracy": float(specy(TresholdValue, genome))})

    prince = max(organism, key=lambda x: x['Accuracy'])
    # king1 = {"Epoch": epoha, "Genome": king["Genome"], "Accuracy": float(specy(TresholdValue, king["Genome"]))}
    if prince["Accuracy"] >= king["Accuracy"]:
        king = prince
        filename = "kings.txt"
        with open(filename, 'a') as out:
            out.write(str(king) + '\n')
            # print(king)

    if 1 == 0:
        print("=======================================================================")
        print()
        print()
        print("Epoch num is " + str(epoha))
        print("- - - - - - - - - - - - -")
        print("King is:")
        print(king)
    bb = 100 * epoha / Epos
    bar.update(bb)
    # print(epoha)
    if king["Accuracy"] > 98.0:
        break
bar.finish()
print()
print()
print("=======================================================================")
print()
print()
print("Epoch num is " + str(epoha))
print("- - - - - - - - - - - - -")
print("King is:")
print(king)
print("That is all!")
