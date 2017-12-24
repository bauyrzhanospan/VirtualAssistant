#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import urllib.request
from datetime import datetime, timedelta
import pymysql
import re


# This function checks time of the order and rule
# And if they are equal -> sends rule
def checkTime(order, rules):
    now = datetime.now()
    now = timedelta(0, int(now.second) + int(now.minute) * 60 + int(now.hour) * 3600)
    for rule in rules:
        if rule["start"] <= now <= rule["stop"] and str(order[0]).lower() == rule["device"] and order[1] == int(
                rule["status"]):
            return rule
        else:
            return None


# This function connects to database and receives rules
# Return rules as a dictionary
def importrules():
    con = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user=None, passwd=None, db='virtass')
    cur = con.cursor(pymysql.cursors.DictCursor)
    with con:
        cur.execute('SELECT * FROM rules')
        dataset = cur.fetchall()
    return dataset


# This function imports preferences of users
# Return preferences as a dictionary
def importprefs():
    con = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user=None, passwd=None, db='virtass')
    cur = con.cursor(pymysql.cursors.DictCursor)
    with con:
        cur.execute('SELECT * FROM preferences')
        dataset = cur.fetchall()
    return dataset


# This function checks if the device is in the status user needs
# If device status == order -> return 1
# Else return 0
def check_same(order):
    try:
        data = urllib.request.urlopen("http://10.12.102.156/port_3480/data_request?id=lu_status").read()
        d = data.decode("utf-8")
        if order.lower() == "KettleOff".lower():
            device = 19
            status = 0
            Status = int(d.split('"id": ' + str(device))[1].split('" }', 1)[0].strip()[-1])
            if Status == status:
                return 1
            else:
                return 0
        elif order.lower() == "KettleOn".lower():
            device = 19
            status = 1
            Status = int(d.split('"id": ' + str(device))[1].split('" }', 1)[0].strip()[-1])
            if Status == status:
                return 1
            else:
                return 0
        elif order.lower() == "LampOn".lower():
            device = 395
            status = 1
            try:
                Status = int(d.split('"id": ' + str(device))[1].split('" }', 1)[0].strip()[-1])
            except ValueError:
                Status = 0
            if Status == status:
                return 1
            else:
                return 0
        elif order.lower() == "LampOff".lower():
            device = 395
            status = 0
            try:
                Status = int(d.split('"id": ' + str(device))[1].split('" }', 1)[0].strip()[-1])
            except ValueError:
                Status = 0
            if Status == status:
                return 1
            else:
                return 0
    except ValueError:
        return 0
    return 0


# This function returns user type of user from database
def Usertype(username):
    con = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user=None, passwd=None, db='virtass')
    cur = con.cursor(pymysql.cursors.DictCursor)
    dataset = {}
    with con:
        cur.execute('SELECT * FROM preferences')
        dataset = cur.fetchall()
    for el in dataset:
        if el["user"] == username:
            return el["usertype"]
    return ""


# This is the Rule Based Reasoner
# It imports order and username
def RBR(order, username):
    # It calls rules importer
    rules = importrules()
    order2 = order

    # It parse order type
    orderDevice = re.sub('[On]', '', order2)
    orderDevice = re.sub('[Off]', '', orderDevice)
    if order[-1] == "n":
        orderStatus = 0
    else:
        orderStatus = 1
    orderdata = [orderDevice, orderStatus]

    # It checks for conflict
    # 0 - device in the same status
    # 1 - you have no enough power
    # 2 - device is changed - it is ok
    if check_same(order) == 1:
        return 0, {"Hello": "No conflict"}
    else:
        conflictrule = checkTime(orderdata, rules)
        if str(conflictrule) != "0":
            return 1, conflictrule
        else:
            return 2, {"Hello": "No conflict"}
