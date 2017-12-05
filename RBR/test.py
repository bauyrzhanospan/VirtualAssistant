import urllib.request
from datetime import datetime, time, timedelta
import pymysql


# from CBR.CBR import Use as cbr

def checkTime(rules):
    now = datetime.now()
    now = timedelta(0, int(now.second) + int(now.minute) * 60 + int(now.hour) * 3600)
    for rule in rules:
        if now >= rule["start"] and now <= rule["stop"]:
            return rule
    return "0"


def importrules():
    con = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user=None, passwd=None, db='virtass')
    cur = con.cursor(pymysql.cursors.DictCursor)
    dataset = {}
    with con:
        cur.execute('SELECT * FROM rules')
        dataset = cur.fetchall()
    return dataset


def importprefs():
    con = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user=None, passwd=None, db='virtass')
    cur = con.cursor(pymysql.cursors.DictCursor)
    dataset = {}
    with con:
        cur.execute('SELECT * FROM preferences')
        dataset = cur.fetchall()
    return dataset


def check_same(order):
    data = urllib.request.urlopen("http://10.12.102.156/port_3480/data_request?id=lu_status").read()
    d = data.decode("utf-8")
    if order == "KettleOff":
        device = 19
        status = 0
        Status = int(d.split('"id": ' + str(device))[1].split('" }', 1)[0].strip()[-1])
        if Status == status:
            return 1
        else:
            return 0
    elif order == "KettleOn":
        device = 19
        status = 1
        Status = int(d.split('"id": ' + str(device))[1].split('" }', 1)[0].strip()[-1])
        if Status == status:
            return 1
        else:
            return 0
    elif order == "LampOn":
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
    elif order == "LampOff":
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
    return 0


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


def RBR(order, usertype):
    rules = importrules()
    prefs = importprefs()
    if check_same(order) == 1:
        return 0
    else:
        if str(checkTime(rules)) != "0":
            test = []
            # cbr(test)


print(Usertype("father"))
