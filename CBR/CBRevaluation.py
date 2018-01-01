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
usersList = {"adult": 1, "young": 2, "elder": 3}


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
                        casesRaw[k]["reasonIN"] = n
                    except KeyError:
                        n = 10
                if casesRaw[k]["usertypeOUT"] == prefRaw[l]["usertype"]:
                    try:
                        n = prefRaw[l][str(casesRaw[k]["reasonOUT"])]
                        casesRaw[k]["reasonOUT"] = n
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


# Function that loads cases and without preferences
def loadOLD():
    with con:
        cur.execute('SELECT * FROM cases')
        casesRaw = list(cur.fetchall())
        cases = []
        casesDict = \
            {"energyI": 0, "entertainmentI": 0, "foodI": 0, "healthI": 0, "securityI": 0, "workI": 0, "usertypeI": 0,
             "energyO": 0, "entertainmentO": 0, "foodO": 0, "healthO": 0, "securityO": 0, "workO": 0, "usertypeO": 0,
             "output": 0, "id": 0}

        # For each element of table is stored into list of training and test sets
        for k in range(len(casesRaw)):
            casesDict["output"] = casesRaw[k]["output"]
            casesDict[str(casesRaw[k]["reasonIN"] + "I")] = 1
            casesDict[str(casesRaw[k]["reasonOUT"] + "O")] = 1
            casesDict["usertypeI"] = usersList[casesRaw[k]["usertypeIN"]]
            casesDict["usertypeO"] = usersList[casesRaw[k]["usertypeOUT"]]
            newCase = copy.deepcopy(casesDict)
            cases.append(newCase)
            casesDict[str(casesRaw[k]["reasonIN"] + "I")] = 0
            casesDict[str(casesRaw[k]["reasonOUT"] + "O")] = 0
            casesDict["usertypeI"] = 0
            casesDict["usertypeO"] = 0
    # Creating training and test set and return it
    training = copy.deepcopy(cases)
    test = copy.deepcopy(cases)
    return training, test


# Function that loads cases and with preferences
def loadOLD2():
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
def specy(covmx, test1, training1):
    trainingRaw = []
    test = copy.deepcopy(test1)
    training = copy.deepcopy(training1)
    for mem in training:
        trainingRaw.append(mem["output"])

    for el in range(len(training)):
        del (training[el]["output"])
        del (training[el]["id"])
    del (test["output"])
    del (test["id"])
    invcovmx = covmx

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
def Accuracy(weights, test, training):
    acc = 0
    for el in range(len(test)):
        testing = copy.deepcopy(test[el])
        resp = specy(weights, testing, training)
        if resp == test[el]['output']:
            acc = acc + 1
    return (acc / len(test)) * 100.0


def Evaluation():
    # New style
    print("Calculation of accuracy for Without Preferences: ")
    training, testFull = load()
    print("Typical input is: ")
    print(training[0])
    # Creating Mahalanobis distance
    trainM = copy.deepcopy(training)
    for el in range(len(trainM)):
        del (trainM[el]["output"])
        del (trainM[el]["id"])
    df = pd.DataFrame(trainM)
    Mahalanobis = df.cov()
    MahalanobisINV = sp.linalg.inv(Mahalanobis)
    print("Accuracy is: ")
    print(Accuracy(MahalanobisINV, testFull, testFull))
    print("====================================================================")

    # Without preferences old style
    print("Calculation of accuracy for Without Preferences: ")
    training1, testFull1 = loadOLD()
    print("Typical input is: ")
    print(training1[0])
    # Creating Mahalanobis distance
    trainM1 = copy.deepcopy(training1)
    for el in range(len(trainM1)):
        del (trainM1[el]["output"])
        del (trainM1[el]["id"])
    df1 = pd.DataFrame(trainM1)
    Mahalanobis1 = df1.cov()
    MahalanobisINV1 = sp.linalg.inv(Mahalanobis1)
    print("Accuracy is: ")
    print(Accuracy(MahalanobisINV1, testFull1, testFull1))
    print("====================================================================")

    # With preferences old style
    print("Calculation of accuracy for Without Preferences: ")
    trainingO2, testFullO2 = loadOLD2()
    print("Typical input is: ")
    print(trainingO2[0])
    # Creating Mahalanobis distance
    trainMO2 = copy.deepcopy(trainingO2)
    for el in range(len(trainMO2)):
        del (trainMO2[el]["output"])
        del (trainMO2[el]["id"])
    dfO2 = pd.DataFrame(trainMO2)
    MahalanobisO2 = dfO2.cov()
    MahalanobisINVO2 = sp.linalg.inv(MahalanobisO2)
    print("Accuracy is: ")
    print(Accuracy(MahalanobisINVO2, testFullO2, testFullO2))
    print("====================================================================")




Evaluation()
