import operator
from itertools import permutations
import itertools
import random
import numpy as np
import time
import datetime
import pymysql
import pandas as pd
import scipy as sp
from scipy.spatial.distance import mahalanobis

con = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user="root", passwd="123", db='virtass')
cur = con.cursor(pymysql.cursors.DictCursor)

prefList = {"energy": 0, "entertainment": 1, "food": 2, "health": 3, "security": 4, "work": 5}
usersList = {"adult": 0.6, "young": 0.3, "elder": 0.6}


def load():
    with con:
        cur.execute('SELECT * FROM cases')
        casesRaw = list(cur.fetchall())
        cur.execute('SELECT * FROM preferences')
        prefRaw = list(cur.fetchall())
        for k in range(len(casesRaw)):
            for l in range(len(prefRaw)):
                if casesRaw[k]["usertypeIN"] == prefRaw[l]["usertype"]:
                    try:
                        n = float(prefRaw[l][str(casesRaw[k]["reasonIN"])])
                        casesRaw[k]["reasonIN"] = n / 10
                    except KeyError:
                        n = 10
                if casesRaw[k]["usertypeOUT"] == prefRaw[l]["usertype"]:
                    try:
                        n = prefRaw[l][str(casesRaw[k]["reasonOUT"])]
                        casesRaw[k]["reasonOUT"] = n / 10
                    except KeyError:
                        n = 10
            try:
                casesRaw[k]["usertypeIN"] = usersList[casesRaw[k]["usertypeIN"]]
                casesRaw[k]["usertypeOUT"] = usersList[casesRaw[k]["usertypeOUT"]]
            except KeyError:
                n = 10

    training = casesRaw
    test = list(casesRaw[:])
    return training, test


def specy(covmx, test):
    training, f = load()
    trainingRaw = []
    for mem in training:
        trainingRaw.append(mem["output"])

    for el in range(len(training)):
        del (training[el]["output"])
        del (training[el]["id"])
    del (test["output"])
    del (test["id"])
    try:
        invcovmx = sp.linalg.inv(covmx)
    except:
        return 2

    tests = [test["reasonIN"], test["reasonOUT"],
             test["usertypeIN"], test["usertypeOUT"]]

    distances = []
    for k in range(len(training)):
        trains = [training[k]["reasonIN"], training[k]["reasonOUT"],
                  training[k]["usertypeIN"], training[k]["usertypeOUT"]]
        distance = mahalanobis(trains, tests, invcovmx)
        distances.append([k, distance])

    classVotes = {}
    for x in range(len(distances)):
        response = distances[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(0), reverse=False)
    for el in distances:
        if el[1] == sortedVotes[0][0]:
            key = el[0]
            break
        else:
            key = el[0]
    response = trainingRaw[key]
    return response


def Accuracy(weights):
    training, test = load()
    acc = 0
    for el in range(len(test)):
        testing = test[el].copy()
        resp = specy(weights, testing)
        if resp == test[el]["output"]:
            acc = acc + 1
    return (acc / len(test)) * 100.0


def train():
    training, f = load()
    for el in range(len(training)):
        del (training[el]["output"])
        del (training[el]["id"])
    training1 = [{'usertypeIN': 0.0, 'reasonOUT': 0.0, 'usertypeOUT': 0.0, 'reasonIN': 0.0},
                 {'usertypeIN': 0.0, 'reasonOUT': 0.0, 'usertypeOUT': 0.0, 'reasonIN': 0.0}]
    df = pd.DataFrame(training1)
    covmx = df.cov()
    genome = covmx.round(3)
    start_time = time.time()
    king = {"Epoch": 0, "Genome": genome, "Accuracy": float(Accuracy(genome))}
    speed = time.time() - start_time
    Epos = 100000
    Deep = 1
    print("Number of epochs is " + str(Epos))
    execution_time = 1.1 * speed * Epos * Deep * int(100)
    print("Estimated execution time is " + str(datetime.timedelta(seconds=int(execution_time))))
    print("Estimated execution time for one epoch is " + str(
        datetime.timedelta(seconds=int(execution_time / 100000))))
    print("=======================================================================")
    print("Starting evolutional algorithm: ")
    bb = 0
    # Write the head of file
    filename = "kings.txt"
    with open(filename, 'a') as out:
        str1 = "Number of epochs is " + str(Epos) + "\n" + "Deepness of the analysis is " + str(Deep) + "\n" + \
               "Estimated execution time is " + str(datetime.timedelta(seconds=int(execution_time))) + "\n " + \
               "Genetic algorithms optimisation for KNN with preference weights" + "\n" + "=" * 20 + "\n"
        out.write(str1)

    items = [-0.001, -0.01, 0, 0, 0.001, 0.01, -0.1, -0.0001, 0, 0, 0.1, 0.0001]
    newI = []
    for p in permutations(items, 4):
        newI.append(list(p))
    newI.sort()
    newI = list(newI for newI, _ in itertools.groupby(newI))

    for epoha in range(Epos):
        organism = [king]
        for x in range(Deep):
            for k in range(100):

                secure_random = random.SystemRandom()
                newW = [list(secure_random.choice(newI)) for k in range(4)]

                new_weight = pd.DataFrame(np.array(newW))
                new_weight.columns = ['reasonIN', 'reasonOUT', 'usertypeIN', 'usertypeOUT']
                new_weight = new_weight.set_index([['reasonIN', 'reasonOUT', 'usertypeIN', 'usertypeOUT']])
                genome = genome.add(new_weight)
                try:
                    organism.append({"Epoch": epoha, "Genome": genome, "Accuracy": float(Accuracy(genome))})
                except:
                    organism.append({"Epoch": epoha, "Genome": genome, "Accuracy": float(0)})

        prince = max(organism, key=lambda x: x['Accuracy'])
        if float(prince["Accuracy"]) >= float(king["Accuracy"]):
            king = prince.copy()
            filename = "kings.txt"
            print("King is dead, new king is now!")
            with open(filename, 'a') as out:
                out.write(str(king) + '\n')

        bb = 100 * epoha / Epos
        print("Percentage is: " + str(bb))
        print("Prince accuracy is " + str(prince['Accuracy']))
        print("Prince genome is: ")
        print(prince["Genome"])
        print("==============")
        print("And king is: " + str(king["Accuracy"]))
        print("King genome is: ")
        print(king["Genome"])
        print("----------------------")
        genome = king["Genome"]
        if king["Accuracy"] > 98:
            break
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


def main(usertypein, usertypeout, reasonin, reasonout):
    test = [str.lower(usertypein), str.lower(usertypeout), str.lower(reasonin), str.lower(reasonout)]
    return test


train()
