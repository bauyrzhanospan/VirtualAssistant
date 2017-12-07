import math
import operator
import random
import sys
import progressbar
import time
import datetime
import pymysql

con = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user=None, passwd=None, db='virtass')
cur = con.cursor()

prefList = {"energy": 0, "entertainment": 1, "food": 2, "health": 3, "security": 4, "work": 5}
usersList = {"adult": 0.6, "young": 0.3, "elder": 0.6}


def loadDataset(split, trainingSet=[], testSet=[]):
    with con:
        cur.execute('SELECT * FROM cases')
        casesRaw = list(cur.fetchall())
        casesTemp = []
        cases = []
        for x in casesRaw:
            casesTemp.append(list(x[1:]))

        cur.execute('SELECT * FROM preferences')
        prefRaw = list(cur.fetchall())
        pref = []
        prefDict = {}
        for el in prefRaw:
            pref.append(list(el[2:]))
            weightsRaw = [0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
            weights = [weightsRaw[x] for x in list(el[3:])]
            prefTemp = {el[2]: weights}
            prefDict.update(prefTemp)

        for case in casesTemp:
            c = [0] * 6
            co = [0] * 6
            c[prefList[case[2]]] = prefDict[case[0]][prefList[case[2]]]
            co[prefList[case[3]]] = prefDict[case[1]][prefList[case[3]]]
            caseTemp = [usersList[case[0]]]
            caseTemp.extend(c)
            caseTemp.append(usersList[case[1]])
            caseTemp.extend(co)
            caseTemp.append(case[-1])
            cases.append(caseTemp)
        # print(cases)
        random.shuffle(cases)

        #        print(cases)
        for x in range(len(cases)):
            trainingSet.append(cases[x])
            testSet.append(cases[x])



def loadDatasetNOpref(split, trainingSet=[], testSet=[]):
    with con:
        cur.execute('SELECT * FROM cases')
        casesRaw = list(cur.fetchall())
        casesTemp = []
        cases = []
        for x in casesRaw:
            casesTemp.append(list(x[1:]))

        cur.execute('SELECT * FROM preferences')
        prefRaw = list(cur.fetchall())
        pref = []
        prefDict = {}
        for el in prefRaw:
            pref.append(list(el[2:]))
            weightsRaw = [1.0] * 6
            weights = [weightsRaw[x] for x in list(el[3:])]
            prefTemp = {el[2]: weights}
            prefDict.update(prefTemp)

        for case in casesTemp:
            c = [0] * 6
            co = [0] * 6
            c[prefList[case[2]]] = prefDict[case[0]][prefList[case[2]]]
            co[prefList[case[3]]] = prefDict[case[1]][prefList[case[3]]]
            caseTemp = [usersList[case[0]]]
            caseTemp.extend(c)
            caseTemp.append(usersList[case[1]])
            caseTemp.extend(co)
            caseTemp.append(case[-1])
            cases.append(caseTemp)
        # print(cases)
        random.shuffle(cases)
        #        print(cases)
        for x in range(len(cases)):
            trainingSet.append(cases[x])
            testSet.append(cases[x])


def loadDataset2():
    trainingSet = []
    with con:
        cur.execute('SELECT * FROM cases')
        casesRaw = list(cur.fetchall())
        casesTemp = []
        cases = []
        for x in casesRaw:
            casesTemp.append(list(x[1:]))

        cur.execute('SELECT * FROM preferences')
        prefRaw = list(cur.fetchall())
        pref = []
        prefDict = {}
        for el in prefRaw:
            pref.append(list(el[2:]))
            weightsRaw = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
            weights = [weightsRaw[x] for x in list(el[3:])]
            prefTemp = {el[2]: weights}
            prefDict.update(prefTemp)

        for case in casesTemp:
            c = [0] * 6
            co = [0] * 6
            c[prefList[case[2]]] = prefDict[case[0]][prefList[case[2]]]
            co[prefList[case[3]]] = prefDict[case[1]][prefList[case[3]]]
            caseTemp = [usersList[case[0]]]
            caseTemp.extend(c)
            caseTemp.append(usersList[case[1]])
            caseTemp.extend(co)
            caseTemp.append(case[-1])
            cases.append(caseTemp)
        for x in range(len(cases)):
            trainingSet.append(cases[x])
    return trainingSet


def loadtest(test):
    trainingSet = []
    with con:
        casesTemp = [test]
        cases = []

        cur.execute('SELECT * FROM preferences')
        prefRaw = list(cur.fetchall())
        pref = []
        prefDict = {}
        for el in prefRaw:
            pref.append(list(el[2:]))
            weightsRaw = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
            weights = [weightsRaw[x] for x in list(el[3:])]
            prefTemp = {el[2]: weights}
            prefDict.update(prefTemp)

        for case in casesTemp:
            c = [0] * 6
            co = [0] * 6
            c[prefList[case[2]]] = prefDict[case[0]][prefList[case[2]]]
            co[prefList[case[3]]] = prefDict[case[1]][prefList[case[3]]]
            caseTemp = [usersList[case[0]]]
            caseTemp.extend(c)
            caseTemp.append(usersList[case[1]])
            caseTemp.extend(co)
            caseTemp.append(case[-1])
            cases.append(caseTemp)
        for x in range(len(cases)):
            trainingSet.append(cases[x])
    return trainingSet


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
    neighbors = []
    for x in range(len(distances)):
        if distances[x][1] <= k:
            neighbors.append(distances[x][0])
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
    predictions = []
    for x in range(len(testSet)):
        neighbors = getNeighbors(trainingSet, testSet[x], TrescholdValue, weights)
        result = getResponse(neighbors)
        predictions.append(result)
    accuracy = getAccuracy(testSet, predictions)
    return accuracy


def train():
    weights = [float(1)] * 14
    TresholdValue = 0.2
    start_time = time.time()
    king = {"Epoch": 0, "Genome": weights, "Accuracy": float(specy(TresholdValue, weights))}
    speed = time.time() - start_time
    while 1:
        Epos = int(input("Write number of epochs: "))
        Deep = int(input("Write deepness: "))
        print("Number of epochs is " + str(Epos))
        print("Deepness of the analysis is " + str(Deep))
        execution_time = 1.1 * speed * Epos * Deep * int(200)
        print("Estimated execution time is " + str(datetime.timedelta(seconds=int(execution_time))))
        print("Estimated execution time for one epoch is " + str(
            datetime.timedelta(seconds=int(execution_time / 100000))))
        ans = int(input("Is it okay? (type 1 for yes, type 0 for no)"))
        if ans == 1:
            break
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
    # Write the head of file
    filename = "kings.txt"
    with open(filename, 'a') as out:
        str1 = "Number of epochs is " + str(Epos) + "\n" + "Deepness of the analysis is " + str(Deep) + "\n" + \
               "Estimated execution time is " + str(datetime.timedelta(seconds=int(execution_time))) + "\n " + \
               "Genetic algorithms optimisation for KNN with preference weights" + "\n" + "=" * 20
        out.write(str1)

    # Create progress bar
    bar = progressbar.ProgressBar().start()
    bar.update(bb)

    # Execute GA
    genome = weights
    for epoha in range(Epos):
        organism = [king]
        for x in range(Deep):
            for k in range(100):
                new_weight = [float(i) * pow(10.0, -x) for i in
                              [random.SystemRandom().uniform(-1.0, 1.0) for _ in range(14)]]
                genome = [abs(float((x + y))) for x, y in zip(genome, new_weight)]
                organism.append({"Epoch": epoha, "Genome": genome, "Accuracy": float(specy(TresholdValue, genome))})
        prince = max(organism, key=lambda x: x['Accuracy'])
        if prince["Accuracy"] >= king["Accuracy"]:
            king = prince
            filename = "kings.txt"
            with open(filename, 'a') as out:
                out.write(str(king) + '\n')

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
        if king["Accuracy"] > 99.8:
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
    with open(filename, 'a') as out:
        str1 = "=" * 20
        str1 = str1 + "Number of epochs is " + str(Epos) + "\n" + "Deepness of the analysis is " + str(Deep) + "\n" + \
               "Estimated execution time is " + str(datetime.timedelta(seconds=int(execution_time))) + "\n " + \
               "Genetic algorithms optimisation for KNN with preference weights" + "\n" + "The king is: \n" + str(king) \
               + "\n" + "=" * 20
        out.write(str1)
    trainNoPref(Epos, Deep)


def trainNoPref(Epos, Deep):
    weights = [float(1)] * 14
    TresholdValue = 0.2
    king = {"Epoch": 0, "Genome": weights, "Accuracy": float(specy(TresholdValue, weights))}
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
    # Write the head of file
    filename = "kings.txt"
    with open(filename, 'a') as out:
        str1 = "Number of epochs is " + str(Epos) + "\n" + "Deepness of the analysis is " + str(Deep) + "\n" + \
               "Genetic algorithms optimisation for KNN without preference weights" + "\n" + "=" * 20
        out.write(str1)

    # Create progress bar
    bar = progressbar.ProgressBar().start()
    bar.update(bb)

    # Execute GA
    genome = weights
    for epoha in range(Epos):
        organism = [king]
        for x in range(Deep):
            for k in range(100):
                new_weight = [float(i) * pow(10.0, -x) for i in
                              [random.SystemRandom().uniform(-1.0, 1.0) for _ in range(14)]]
                genome = [abs(float((x + y))) for x, y in zip(genome, new_weight)]
                organism.append({"Epoch": epoha, "Genome": genome, "Accuracy": float(specy(TresholdValue, genome))})
        prince = max(organism, key=lambda x: x['Accuracy'])
        if prince["Accuracy"] >= king["Accuracy"]:
            king = prince
            filename = "kings.txt"
            with open(filename, 'a') as out:
                out.write(str(king) + '\n')

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
        if king["Accuracy"] > 99.8:
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
    with open(filename, 'a') as out:
        str1 = "=" * 20
        str1 = str1 + "Number of epochs is " + str(Epos) + "\n" + "Deepness of the analysis is " + str(Deep) + "\n" + \
               "Genetic algorithms optimisation for KNN without preference weights" + "\n" + "The king is: \n" + str(
            king) \
               + "\n" + "=" * 20
        out.write(str1)


def Use(test):
    # Test value is smt like this:
    # 0.3, 0.5, 0, 0, 0, 0, 0, 0.9, 0, 0.3, 0, 0, 0, 0
    # usertype - 6 inputs: usertype - 6 inputs
    print(loadtest(test))
    test = loadtest(test)

    # Genome taken from log txt = kings.txt
    weights = [62.74296408346383, 45.16062627967977, 153.81119791760204, 24.020401442716725, 231.98382020356667,
               144.38153135366565, 99.80322782656873, 30.678550967108613, 215.8497441122619, 113.33037913748292,
               178.47764325147978, 80.75715293524664, 137.13264707612845, 110.04931317113186]
    return getResponse(getNeighbors(loadDataset2(), test, 0.9, weights))


def main(usertypein, usertypeout, reasonin, reasonout):
    test = [str.lower(usertypein), str.lower(usertypeout), str.lower(reasonin), str.lower(reasonout)]
    return Use(test)
