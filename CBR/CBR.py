import operator
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
    test = list(casesRaw[0::3])
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

    df = pd.DataFrame(training)
    covmx = df.cov()

    genome = covmx

    start_time = time.time()
    king = {"Epoch": 0, "Genome": genome, "Accuracy": float(Accuracy(genome))}
    speed = time.time() - start_time
    Epos = 1000
    Deep = 1
    print("Number of epochs is " + str(Epos))
    print("Deepness of the analysis is " + str(Deep))
    execution_time = 1.1 * speed * Epos * Deep * int(200)
    print("Estimated execution time is " + str(datetime.timedelta(seconds=int(execution_time))))
    print("Estimated execution time for one epoch is " + str(
        datetime.timedelta(seconds=int(execution_time / 100000))))
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
               "Genetic algorithms optimisation for KNN with preference weights" + "\n" + "=" * 20 + "\n"
        out.write(str1)

    for epoha in range(Epos):
        organism = [king]
        organs = []
        for x in range(Deep):
            for k in range(100):

                new_weight = pd.DataFrame(np.random.randn(4, 4))
                new_weight.columns = ['reasonIN', 'reasonOUT', 'usertypeIN', 'usertypeOUT']
                new_weight = new_weight.set_index([['reasonIN', 'reasonOUT', 'usertypeIN', 'usertypeOUT']])
                genome = genome.dot(new_weight)
                try:
                    organism.append({"Epoch": epoha, "Genome": genome, "Accuracy": float(Accuracy(genome))})
                    organs.append({"Epoch": epoha, "Genome": genome, "Accuracy": float(Accuracy(genome))})
                except:
                    organism.append({"Epoch": epoha, "Genome": genome, "Accuracy": float(0)})
                    organs.append({"Epoch": epoha, "Genome": genome, "Accuracy": float(Accuracy(genome))})

        prince = max(organism, key=lambda x: x['Accuracy'])
        prince2 = max(organs, key=lambda x: x['Accuracy'])
        print("Prince for epoh " + str(epoha) + " is " + str(prince2))
        if prince["Accuracy"] >= king["Accuracy"]:
            king = prince
            filename = "kings.txt"
            with open(filename, 'a') as out:
                out.write(str(king) + '\n')

        bb = 100 * epoha / Epos
        print("Percentage is: " + str(bb) + " and accuracy is: " + str(king["Accuracy"]))
        # print(epoha)
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
