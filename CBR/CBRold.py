#!/usr/bin/python3
# -*- coding: UTF-8 -*-
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
import copy

# Connect to db
con = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user="root", passwd="123", db='virtass')
cur = con.cursor(pymysql.cursors.DictCursor)

# Put coefficients of reasons and preferences
prefList = {"energy": 0, "entertainment": 1, "food": 2, "health": 3, "security": 4, "work": 5}
usersList = {"adult": 0.6, "young": 0.3, "elder": 0.6}


# Function that loads cases and preferences
def load():
    with con:
        cur.execute('SELECT * FROM cases')
        casesRaw = list(cur.fetchall())
        cur.execute('SELECT * FROM preferences')
        prefRaw = list(cur.fetchall())
        cases = []
        casesDict = \
            {"energyI": 0, "entertainmentI": 0, "foodI": 0, "healthI": 0, "securityI": 0, "workI": 0, "usertypeI": 0,
             "energyO": 0, "entertainmentO": 0, "foodO": 0, "healthO": 0, "securityO": 0, "workO": 0, "usertypeO": 0,
             "output": 0, "id": 0}
        cur.execute('SELECT * FROM preferences')
        prefRaw = list(cur.fetchall())

        # For each element of table is stored into list of training and test sets
        for k in range(len(casesRaw)):
            casesDict["output"] = casesRaw[k]["output"]
            for l in range(len(prefRaw)):
                if casesRaw[k]["usertypeIN"] == prefRaw[l]["usertype"]:
                    casesDict[str(casesRaw[k]["reasonIN"] + "I")] = prefRaw[l][str(casesRaw[k]["reasonIN"])]
                if casesRaw[k]["usertypeOUT"] == prefRaw[l]["usertype"]:
                    casesDict[str(casesRaw[k]["reasonOUT"] + "O")] = prefRaw[l][str(casesRaw[k]["reasonOUT"])]
                casesDict["usertypeI"] = usersList[casesRaw[k]["usertypeIN"]]
                casesDict["usertypeO"] = usersList[casesRaw[k]["usertypeOUT"]]
                newCase = copy.deepcopy(casesDict)
                cases.append(newCase)
                casesDict[str(casesRaw[k]["reasonIN"] + "I")] = 0
                casesDict[str(casesRaw[k]["reasonOUT"] + "O")] = 0
                casesDict["usertypeI"] = 0
                casesDict["usertypeO"] = 0
    # Creating training and test set and return it
    training = cases
    test = cases
    return training, test


# Pure CBR, calculating Mahalanobis distance and find nearest case and return it back
def specy(weights, test):
    training, f = load()
    trainingRaw = []

    try:
        invcovmx = sp.linalg.inv(weights)
    except:
        return 2

    tests = list(test.values())

    distances = []
    for k in range(len(training)):
        trains = list(training[k].values())
        distance = mahalanobis(trains, tests, invcovmx)  # Calculating Mahalanobis distance
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


# Calculate Accuracy of genome by compaing its values with predefined outputs, return accuracy percentage
def Accuracy(weights):
    training, test = load()
    acc = 0
    for el in range(len(test)):
        testing = test[el].copy()
        resp = specy(weights, testing)
        if resp == test[el]["output"]:
            acc = acc + 1
    return (acc / len(test)) * 100.0


# Fun starts here, this is genetic algorithm to find best Mahalanobis matrix
def train():
    training, f = load()
    for el in range(len(training)):
        del (training[el]["output"])
        del (training[el]["id"])

    # Creating Mahalanobis Matrix of zeros and store it in genome
    training1 = [
        {"energyI": 0, "entertainmentI": 0, "foodI": 0, "healthI": 0, "securityI": 0, "workI": 0, "usertypeI": 0,
         "energyO": 0, "entertainmentO": 0, "foodO": 0, "healthO": 0, "securityO": 0, "workO": 0, "usertypeO": 0},
        {"energyI": 0, "entertainmentI": 0, "foodI": 0, "healthI": 0, "securityI": 0, "workI": 0,
         "usertypeI": 0,
         "energyO": 0, "entertainmentO": 0, "foodO": 0, "healthO": 0, "securityO": 0, "workO": 0,
         "usertypeO": 0}]
    df = pd.DataFrame(training1)
    covmx = df.cov()
    genome = covmx.round(3)

    # Calculating time of execution
    start_time = time.time()
    king = {"Epoch": 0, "Genome": genome, "Accuracy": float(Accuracy(genome))}
    speed = time.time() - start_time
    Epos = 10000  # Defining number of epochs in training algorithm
    Deep = 1  # Deepness of the GA, don`t change
    print("Number of epochs is " + str(Epos))
    execution_time = 1.1 * speed * Epos * Deep * int(100)  # Execution time of the GA
    print("Estimated execution time is " + str(datetime.timedelta(seconds=int(execution_time))))
    print("Estimated execution time for one epoch is " + str(
        datetime.timedelta(seconds=int(execution_time / 100000))))
    print("=======================================================================")
    print("Starting evolutional algorithm: ")

    # Write the head of log file
    filename = "kings.txt"
    with open(filename, 'a') as out:
        str1 = "Number of epochs is " + str(Epos) + "\n" + "Deepness of the analysis is " + str(Deep) + "\n" + \
               "Estimated execution time is " + str(datetime.timedelta(seconds=int(execution_time))) + "\n " + \
               "Genetic algorithms optimisation for KNN with preference weights" + "\n" + "=" * 20 + "\n"
        out.write(str1)
    # Creating mutation patterns
    newI = [-0.0001, -0.001, -0.01, -0.1, 0, 0.1, 0.001, 0.0001]  # Mutation types
    # Genetic algorithm
    for epoha in range(Epos):
        organism = [king]  # King is the part of choose
        for x in range(Deep):
            for k in range(100):
                # Secure random selection of mutation pattern, it uses os.random to make it trully random
                secure_random = random.SystemRandom()
                newW = []
                for m in range(14):
                    newM = [list(secure_random.choice(newI)) for k in range(14)]
                    newW.append(newM)
                # Creating new genome of specy and checking its accuracy level
                new_weight = pd.DataFrame(np.array(newW))
                new_weight.columns = ['reasonIN', 'reasonOUT', 'usertypeIN', 'usertypeOUT']
                new_weight = new_weight.set_index([['reasonIN', 'reasonOUT', 'usertypeIN', 'usertypeOUT']])
                genome = genome.add(new_weight)
                try:
                    organism.append({"Epoch": epoha, "Genome": genome, "Accuracy": float(Accuracy(genome))})
                except:
                    organism.append({"Epoch": epoha, "Genome": genome, "Accuracy": float(0)})
        # Defining its best result
        prince = max(organism, key=lambda x: x['Accuracy'])
        # If prince`s accuracy better than king`s, then new king is here
        if float(prince["Accuracy"]) >= float(king["Accuracy"]):
            # It writes it to kings.txt log file
            king = prince.copy()
            filename = "kings.txt"
            print("King is dead, new king is now!")
            with open(filename, 'a') as out:
                out.write(str(king) + '\n')
        # Prompt results of the algorithm
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
        # If accuracy is better than 98%, then -> break GA
        if king["Accuracy"] > 95:
            break
    # Print out results
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


# Function to use CBR by other part, takes case and returns decision
def main(usertypein, usertypeout, reasonin, reasonout):
    weights = [[1.5882, -0.3039, -1.1047, 0.6826], [-0.7584, 0.2737, 0.1781, -0.2904],
               [0.1010, 0.0266, 0.3134, -0.8066],
               [-0.3870, -0.0481, -0.1985, -0.7557]]  # It is the best genome found by GA (genetic algorithm) kings.txt
    new_weight = pd.DataFrame(np.array(weights))
    new_weight.columns = ['reasonIN', 'reasonOUT', 'usertypeIN', 'usertypeOUT']
    new_weight = new_weight.set_index([['reasonIN', 'reasonOUT', 'usertypeIN', 'usertypeOUT']])
    test = {'output': 1, 'usertypeIN': str.lower(usertypein), 'reasonIN': str.lower(reasonin),
            'reasonOUT': str.lower(reasonout), 'usertypeOUT': str.lower(usertypeout), 'id': 0}
    return specy(new_weight, test)


train()
