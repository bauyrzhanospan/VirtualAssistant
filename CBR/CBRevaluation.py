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
from random import shuffle

# Connect to db
con = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user="root", passwd="123", db='virtass')
cur = con.cursor(pymysql.cursors.DictCursor)

# Put coefficients of reasons and preferences
prefList = {"energy": 0, "entertainment": 1, "food": 2, "health": 3, "security": 4, "work": 5}
usersList = {"adult": 0.9, "young": 0.3, "elder": 0.6}


# Function that loads cases and preferences
def load():
    with con:
        cur.execute('SELECT * FROM cases')
        casesRaw = list(cur.fetchall())
        cur.execute('SELECT * FROM preferences')
        prefRaw = list(cur.fetchall())

        # For each element of table is stored into list of training and test sets
        for k in range(len(casesRaw)):
            for l in range(len(prefRaw)):
                # Each of the reason is parsed inside global variable and coefficients are put
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
            # Put coefficients from global variables to lists
            try:
                casesRaw[k]["usertypeIN"] = usersList[casesRaw[k]["usertypeIN"]]
                casesRaw[k]["usertypeOUT"] = usersList[casesRaw[k]["usertypeOUT"]]
            except KeyError:
                n = 10
    # Creating training and test set and return it
    training = casesRaw
    test = casesRaw
    return training, test


# Pure CBR, calculating Mahalanobis distance and find nearest case and return it back
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
    invcovmx = covmx

    tests = [test["reasonIN"], test["reasonOUT"],
             test["usertypeIN"], test["usertypeOUT"]]

    distances = []
    for k in range(len(training)):
        trains = [training[k]["reasonIN"], training[k]["reasonOUT"],
                  training[k]["usertypeIN"], training[k]["usertypeOUT"]]
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
def Accuracy(weights, test):
    training, f = load()
    acc = 0
    for el in range(len(test)):
        testing = test[el].copy()
        resp = specy(weights, testing)
        if resp == test[el]["output"]:
            acc = acc + 1
    return (acc / len(test)) * 100.0


def Evaluation():
    training, testFull = load()
    shuffle(testFull)
    # Putting best genome
    weights = [[0.5054, -0.3618, -0.9035, 0.0926],
               [0.3779, 0.0895, 0.0049, -0.0030],
               [0.4400, -0.1455, 0.3397, 0.1160],
               [0.0911, 0.2284, 0.2374, 0.3343]]  # It is the best genome found by GA (genetic algorithm) kings.txt
    Genome = sp.linalg.inv(weights)

    # Creating Mahalanobis matrix
    trainM = copy.deepcopy(training)
    for el in range(len(trainM)):
        del (trainM[el]["output"])
        del (trainM[el]["id"])
    df = pd.DataFrame(trainM)
    Mahalanobis = df.cov()
    MahalanobisINV = sp.linalg.inv(Mahalanobis)

    # Creating identity matrix to convert Mahalanobis Distance to Euclidean Distance
    Euclidean = [[1, 0, 0, 0],
                 [0, 1, 0, 0],
                 [0, 0, 1, 0],
                 [0, 0, 0, 1]]

    # Creating test sets
    test25 = testFull[0::4]
    test10 = testFull[0::10]
    test50 = testFull[0::2]
    print("10% test:")
    print("Euclidean Distance:")
    print(Accuracy(Euclidean, test10))
    print("Mahalanobis Distance:")
    print(Accuracy(MahalanobisINV, test10))
    print("Ospan Matrix Distance:")
    print(Accuracy(Genome, test10))
    print("============================")
    print("25% test:")
    print("Euclidean Distance:")
    print(Accuracy(Euclidean, test25))
    print("Mahalanobis Distance:")
    print(Accuracy(MahalanobisINV, test25))
    print("Ospan Matrix Distance:")
    print(Accuracy(Genome, test25))
    print("============================")
    print("50% test:")
    print("Euclidean Distance:")
    print(Accuracy(Euclidean, test50))
    print("Mahalanobis Distance:")
    print(Accuracy(MahalanobisINV, test50))
    print("Ospan Matrix Distance:")
    print(Accuracy(Genome, test50))
    print("============================")
    print("100% test:")
    print("Euclidean Distance:")
    print(Accuracy(Euclidean, testFull))
    print("Mahalanobis Distance:")
    print(Accuracy(MahalanobisINV, testFull))
    print("Ospan Matrix Distance:")
    print(Accuracy(Genome, testFull))
    print("============================")


Evaluation()
