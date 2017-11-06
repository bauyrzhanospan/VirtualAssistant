import nltk
from nltk.stem.lancaster import LancasterStemmer
import os
import json
import datetime

stemmer = LancasterStemmer()
import numpy as np
import time
import glob
from datetime import datetime, time
from lib import modsOrder as mO
from lib import modsReason as mR


# TODO: commend everything and write good README

# If first user has higher priority than return 1, if less 0, if equal 2
def compare_user(user1, user2):
    users = [user1[:-1], str(user2)]
    k = [5, 5]
    m = 0
    for u in users:
        if str(u) in "adult":
            k[m] = 0
        elif str(u) in "elderly":
            k[m] = 1
        elif str(u) in "young":
            k[m] = 2
        m = m+1
    if k[0]>k[1]:
        return 0
    elif k[0]==k[1]:
        return 2
    else:
        return 1

def find_high(rule):
    users = list(rule["users"])
    k = [5, 5, 5, 5]
    for u in users:
        if str(u) == "adult":
            k[users.index(u)] = 0
        elif str(u) == "elderly":
            k[users.index(u)] = 1
        elif str(u) == "young":
            k[users.index(u)] = 2
    prio = min(k)
    if prio == 0:
        return "adult"
    elif prio == 1:
        return "elderly"
    else:
        return "young"

# TODO: make it unique for users
def check_order():
    words_file = './include/order.json'
    with open(words_file) as word_file:
        order = json.load(word_file)
        if order == 1:
            return 1
        else:
            return 0
# TODO: make it uniqe too
def make_order(Isorder):
    words_file = './include/order.json'
    with open(words_file, "w") as word_file:
        json.dump(Isorder, word_file)
    return "Printed"

def class_order(text):
    order = mO.classify(text)
    try:
        return order[0][0]
    except IndexError:
        return 0

def class_reason(text):
    reason = mR.classify(text)
    try:
        return reason[0][0]
    except IndexError:
        return 0

def compare(reason1, reason2, usertype):
    conf_file = "./Conf/rules.conf"
    print(reason1)
    print(reason2)
    print(usertype)
    with open(conf_file) as file:
        for line in file:
            try:
                data = line.split(":")
                if str(data[0]) in str(usertype.lower()):
                    print("Ok")
                    rules = data[1][:-1].split(",")
                    print(rules)
            except:
                print("There is no rules")
                return None
    if rules.index(reason1.lower()) == rules.index(reason2.lower()):
        return 0
    elif rules.index(reason1.lower()) < rules.index(reason2.lower()):
        return 1
    else:
        return 2

def in_between(now, start, end):
    if start <= end:
        return start <= now < end
    else: # over midnight e.g., 23:30-04:15
        return start <= now or now < end

# TODO: create script to eliminate conflicts between online users
def check_pol(order, username, reason):
    # TODO: make temp politics configuration file, idea is: when smb changes status of the device with enough power, just write this change to the temp politics conf, and when it will be changed, just refresh at specific time.
    conf_file = "./Conf/politics.conf"
    politics = []
    pol = dict.fromkeys(["start", "stop", "users", "device", "preference", "status"])
    with open(conf_file) as file:
        for line in file:
            try:
                data = line.split(':')
                times = data[0].split("-")
                users = data[1].split(",")
                pol["start"] = times[0]
                pol["stop"] = times[1]
                pol["users"] = users
                pol["device"] = data[2]
                pol["status"] = data[3]
                pol["preference"] = data[4][:-1]
                politics.append(pol)
                pol = dict.fromkeys(["start", "stop", "users", "device", "preference", "status"])
            except IndexError:
                return False
    now = datetime.now()
    now_time = now.time()
    noway = []
    bush = []
    if order[-1:] == "f":
        act = "On"
    else:
        act = "Off"
    if order[0] == "K":
        dev = "19"
    else:
        dev = "395"
    for element in politics:
        startHour = int(str(element["start"])[:-2])
        startMin = int(str(element["start"])[-2:])
        stopHour = int(str(element["stop"])[:-2])
        stopMin = int(str(element["stop"])[-2:])
        if in_between(now_time, time(startHour, startMin), time(stopHour, stopMin)) and act == str(element["status"]) and dev == str(element["device"]):
            if compare_user(username, find_high(element)) == 0:
                return 9
            noway.append(politics.index(element))
    if not noway:
        return 0
    else:
        for el in noway:
            bush.append(politics[el])
        if reason == 0:
            return 1
        else:
            for el in bush:
                if compare(el["preference"], reason, username) == 1:
                    return 1
                else:
                    return 0

def device_change(order):
    make_order(0)
    conf_file = "./Conf/timer.conf"
    with open(conf_file) as file:
        for line in file:
            timer = line
    if order == "KettleOff":
        return "Kettle is turned off for " + str(timer) + " minutes"
    elif order == "KettleOn":
        return "Kettle is turned on for " + str(timer) + " minutes"
    elif order == "LampOn":
        return "Lamp is turned on for " + str(timer) + " minutes"
    elif order == "LampOff":
        return "Lamp is turned off for " + str(timer) + " minutes"

def Give_answer(text):
    return device_change(text)

def user_type(user):
    conf_file = "./Conf/users.conf"
    with open(conf_file) as file:
        for line in file:
            try:
                data = line.split(":")
                if user.lower() == data[0].lower():
                    usertype = data[1]
            except:
                return 0
    return usertype

def accounts():
    conf_file = "./Conf/users.conf"
    account = []
    with open(conf_file) as file:
        for line in file:
            try:
                data = line.split(":")
                account.append(data[0])
            except:
                return 0
    return account

# TODO: make it uniq for all users
def write_order(order):
    words_file = './include/GlobalOrders.json'
    if order == 0:
        with open(words_file, "r") as word_file:
            order2 = json.load(word_file)
            return order2
    else:
        with open(words_file, "w") as word_file:
            json.dump(order, word_file)

print(class_reason("danger"))