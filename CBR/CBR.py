#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import operator
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
usersList = {"adult": 3, "young": 2, "elder": 1}


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
    test = list(casesRaw[0::4])
    return training


# Pure CBR, calculating Mahalanobis distance and find nearest case and return it back
def Calculate(covmx, test):
    training = load()
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


# Function to use CBR by other part, takes case and returns decision
def main(usertypein, usertypeout, reasonin, reasonout):
    # Loading cases Database
    training = load()
    trainM = copy.deepcopy(training)
    # Removing output and id coulumns
    for el in range(len(trainM)):
        del (trainM[el]["output"])
        del (trainM[el]["id"])
    # Calculating Conversion matrix
    df = pd.DataFrame(trainM)
    Mahalanobis = df.cov()
    # Restructuring input into readable for program
    test = {'output': 1, 'usertypeIN': usersList[str.lower(usertypein)],
            'reasonIN': float(prefList[str.lower(reasonin)]) / 10,
            'reasonOUT': float(prefList[str.lower(reasonout)]) / 10, 'usertypeOUT': usersList[str.lower(usertypeout)],
            'id': 0}
    # Returning result
    return Calculate(Mahalanobis, test)

