#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import random
import urllib

import pymysql
from flask import Flask, render_template, request, Markup

import DM

app = Flask(__name__)  # Creating new flask app


def write2dbLOG(key, value):  # This is database logging engine, it takes key and value and stores it in eval table

    # Connecting virtass database
    con = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user="root", passwd="123", db='virtass')
    cur = con.cursor(pymysql.cursors.DictCursor)
    # Connecting to the table eval and changing given value with given key
    id = cur.execute("SELECT * FROM `eval` ORDER BY `eval`.`id` ASC LIMIT 10000")
    cur.execute("UPDATE `eval` SET `" + str(key) + "` = '" + str(value)
                + "' WHERE `eval`.`id` = '" + str(id) + "';")
    # Commit and push changes, close database
    con.commit()
    cur.close()
    con.close()


# This module checks status of the devices
# It sends get request to Vera and parses it
def check_status(deviceNum):  # Taking device number to parse its value
    # Sending GET request to the Vera
    # IP of Vera was 10.12.102.156 - if it changed, change it here
    data = urllib.request.urlopen("http://10.12.102.156/port_3480/data_request?id=lu_status").read()

    d = data.decode("utf-8")  # Decoding request
    # Parse status of the device
    try:
        Status = int(d.split('"id": ' + str(deviceNum))[1].split('" }', 1)[0].strip()[-1])
        states = ["off", "on"]
        return states[Status]
    except:
        return "somehow?"


# This is randomiser module
# It creates scenarios for users inside the Evaluation test
def randomiser():
    # It connect to the Database
    con = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user="root", passwd="123", db='virtass')
    cur = con.cursor(pymysql.cursors.DictCursor)
    # Block of software that creates random conflict
    users = ["Father", "Mother", "Son", "Grandpa"]
    usertypes2 = {"Father": "adult", "Mother": "adult", "Son": "young", "Grandpa": "elder"}
    reasons = ["energy", "entertainment", "food", "health", "security", "work"]
    devices = ["lamp"]
    u = random.SystemRandom().choice(users)  # Crypto-secure random choice
    user = usertypes2[u]
    users2 = users
    users2.remove(u)
    u2 = random.SystemRandom().choice(users2)
    user2 = usertypes2[u2]
    reason = random.SystemRandom().choice(reasons)
    dev = random.SystemRandom().choice(devices)
    # It takes GET from Vera to create scenario which is real such that device in the status of rule
    data = urllib.request.urlopen("http://10.12.102.156/port_3480/data_request?id=lu_status").read()
    d = data.decode("utf-8")
    try:
        if dev == "kettle":
            device = 19
        else:
            device = 395
        status = int(d.split('"id": ' + str(device))[1].split('" }', 1)[0].strip()[-1])
    except ValueError:
        status = 0
    # Commit changes and close database
    cur.close()
    con.close()
    # Again connection to the Database, I don`t know why
    con = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user="root", passwd="123", db='virtass')
    cur = con.cursor(pymysql.cursors.DictCursor)
    # Update of information inside the rules table
    cur.execute("UPDATE `rules` SET `user` = '" + str(user2) + "' WHERE `rules`.`id` = 0")
    con.commit()
    cur.execute("UPDATE `rules` SET `reason` = '" + str(reason) + "' WHERE `rules`.`id` = 0")
    con.commit()
    cur.execute("UPDATE `rules` SET `device` = '" + str(dev) + "' WHERE `rules`.`id` = 0")
    con.commit()
    cur.execute("UPDATE `rules` SET `status` = '" + str(status) + "' WHERE `rules`.`id` = 0")
    # Commit and close database
    con.commit()
    cur.close()
    con.close()

    # Add values to eval table, updating evaluation tables by data created before by Randomizer
    con = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user="root", passwd="123", db='virtass')
    cur = con.cursor(pymysql.cursors.DictCursor)
    order = dev.title() + ["On", "Off"][status]
    Newreason = random.SystemRandom().choice(reasons)
    cur.execute("INSERT INTO `eval` (`user`, `otheruser`, `ordertype`, `rulereason`, `reason`) VALUES ('" +
                str(user) + "', '" + str(user2) + "', '" + str(order) + "', '" + str(reason) + "', '" + str(
        Newreason) + "');")
    # Commit and close
    con.commit()
    id23 = cur.execute("SELECT * FROM `eval` ORDER BY `eval`.`id` ASC LIMIT 10000")
    cur.close()
    con.close()

    # Write to answer.txt new Evaluation Instruction
    priorities = {"adult": "highest", "elder": "second highest", "young": "lowest"}
    preferences = {"adult": "1: Security, 2: Health, 3: Work, 4: Food, 5: Energy, 6: Entertainment",
                   "elder": "1: Health, 2: Security, 3: Work, 4: Food, 5: Energy, 6: Entertainment",
                   "young": "1: Security, 2: Work, 3: Entertainment, 4: Health, 5: Food, 6: Energy"}
    priority = priorities[user]
    preference = preferences[user]
    priority2 = priorities[user2]
    preference2 = preferences[user2]

    answer = "Your ID is " + str(id23) + "<br>" + \
             "The system can be used by different users (Father, Mother, Son, Grandpa) that have different " \
             "roles (Adult, Elder, Young).<br>Please, go through the instructions. " \
             "<br><br><h4>Instructions:</h4>" \
             "The system has randomly chosen " \
             "to be user '"
    answer = answer + str(u) + "'.<br>" + str(u) + " is the '" + str(user) + "' usertype which is the " \
             + str(priority) + " priority usertype.<br>" + str(u) + " has the " \
                                                                    "following preferences (1 is the highest):<br>" \
             + str(preference) + "<br>"

    answer = answer + "The other user of the system is the '" + str(u2) + "' with usertype '" + str(
        user2) + "' which is the " \
             + str(priority2) + " priority usertype.<br> The other user '" + str(u2) + "' has the " \
                                                                                       "following preferences:<br>" \
             + str(preference2) + "<br><br>" + "<h5>Conflict:</h5><br>There is a conflict between you (" + \
             str(u) + ":" + str(user) + ") and the other " \
                                        "user (" + str(u2) + ":" + str(
        user2) + ") .<br>The other user turned the " + str(dev) + " " + \
             str(["off", "on"][status]) + " with a reason based on the " + str(reason) + " issue.<br>" + \
             "But you need the device to be in an opposite status because your reason is " + str(Newreason) \
             + " issue.<br> Let`s check how the system will resolve this conflict."
    # Writing to manual.txt new Evaluation test manual
    Manual = "<ol><li>On the login page choose '" + str(u) + "'. </li>" + \
             "<li>Then type or say (by clicking the microphone) in your own words the order to turn " \
             + str(["on", "off"][status]) + " the " + str(dev) + ".</li>" \
             + "<li>Then the system will inform you that there is a conflict and will ask you about " \
               "the next step. Type or say 'yes'." + "</li>" \
             + "<li>Then type or say (by clicking the microphone) in your own words the reason about the " + \
             str(Newreason) + " issue.</li>" + "<li>Then the system resolves the conflict and " \
                                               "you will need to answer the questionnaire." \
                                               "</li></ol>"
    # Creating head of the summary.txt of the evaluation test
    summary = "<h2>Story:</h2><ol><li>Your user is " + str(u) + ", " + str(user) + " usertype (" + str(priority) + \
              " priority) with next preferences:<br>" + str(preference) + "<br></li><li>" + \
              "Other user is " + str(u2) + ", " + str(user2) + " usertype (" + str(priority2) + \
              " priority) with next preferences:<br>" + str(preference2) + "<br></li><li>" + \
              "Conflict: you (" + str(u) + ":" + str(user) + ") want to turn the " + str(dev) + \
              " " + str(["on", "off"][status]) + \
              " but other user (" + str(u2) + ":" + str(user2) + ") did the opposite. </li><li>" + \
              "Other user`s (" + str(u2) + ", " + str(user2) + ") reason is " + str(reason).upper() + \
              "</li><li>Your (" + str(u) + ", " + str(user) + ") reason is: "
    # Writing them down
    with open("answer.txt", 'w') as out:
        out.write(answer)
    with open("manual.txt", 'w') as o:
        o.write(Manual)
    with open("summary.txt", 'w') as o:
        o.write(summary)


# Function to write summary of the Evaluation Test in the end of test
def Summary():
    # Writing header for flask, it will be rendered inside the page
    header = "Summary"
    # Read previously created summary and store it in variable
    with open("summary.txt", 'r') as out:
        summary = out.read()
    # Connect to eval table and take all data about evaluation test
    con = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user="root", passwd="123", db='virtass')
    cur = con.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM `eval`')
    dataset = cur.fetchall()
    # Close table
    cur.close()
    con.close()
    # Parse variables from table
    orderraw = dataset[-1]["orderraw"]
    orderdef = dataset[-1]["orderdef"]
    reasonraw = dataset[-1]["reasonraw"]
    reasondef = dataset[-1]["reasondef"]
    output = dataset[-1]["output"]
    winner = [" other user`s ", " your "][output]
    # Write end of the summary.txt and send it to flask.render
    summary = summary + str(reasondef).upper() + "</li>" + "<li>System desided that" + str(winner) + \
              "order has a higher priority.</li></ol><h2>Classification:</h2><ol><li>Your order was: " + \
              str(orderraw) + "</li><li>System classified order as: " + str(orderdef) + "</li><li>" + \
              "Your reason was: " + str(reasonraw) + "</li><li>" + \
              "System classified reason as: " + str(reasondef) + "</li></ol>"
    answer = Markup(summary)  # Markup used to make the text readable by browser
    return answer, header  # Returning header and info for summary page


# Reading answer.txt and returning it to flask.render after markdown
def readANS():
    with open("answer.txt", 'r') as out:
        answer = out.read()
    Info = Markup(answer)
    header = "Welcome to the evaluation test"
    return Info, header


# Reading manual.txt and returning it to flask.render after markdown
def readMan():
    with open("manual.txt", 'r') as out:
        answer = out.read()
    Info = Markup(answer)
    header = "Manual"
    return Info, header


# Login page, no authorisation with password
# TODO: add password
@app.route("/")  # Root for login page is index "/"
def login():
    randomiser()  # Create scenario and write all data to txt files
    # Read data from txt files and send it to render
    Info, header = readANS()  # Read data from answer.txt files and send it to render
    manual, mheader = readMan()  # Read data from manual.txt files and send it to render
    # Return render of the login.html page with new local variables
    return render_template(
        "login.html", **locals())


# Control page with route defined by username or username and his order
@app.route("/<username>", methods=['GET', 'POST'])
@app.route("/<username>/<order>/", methods=["GET", "POST"])
def orderClassification(username, order="noorder"):  # By default there is no order


    Info, header = readANS()  # Read data from answer.txt files and send it to render  
    manual, mheader = readMan()  # Read data from manual.txt files and send it to render
    # Taking status of devices, updating it
    statusLamp = check_status(395)
    statusKettle = check_status(19)
    text = ''
    # Greeting answer of Virtual Assistant
    answer = "Hello, " + str(username).title() + ", I am your Virtual Assistant. Type or tell me your order."

    if request.method == 'POST':  # If user POST by clicking submit button any text
        text = request.form['text']
        write2dbLOG("orderraw", text)  # Write to database raw version of order
        try:
            responce, answer, conflict, order = DM.DMorder(text, username)  # Taking data from Dialogue Manager
        except IndexError:  # If system did not managed to classify order
            # Render new answer
            answer = "Sorry, I could not classify your order. Please, try again with different phrase."
            smile = Markup("https://github.com/BiggyBaron/VirtualAssistant/blob/master/static/waiting.gif?raw=true")
            order = "noorder"
            return render_template('main.html', **locals())
        write2dbLOG("orderdef", order)  # Write to database classified version of order
        if responce == 0:  # If DM (dialogue manager) send command 0, then there is a conflict, render yesno.html page
            # Taking status of devices, updating it
            statusLamp = check_status(395)
            statusKettle = check_status(19)
            smile = Markup("https://github.com/BiggyBaron/VirtualAssistant/blob/master/static/yesno.gif?raw=true")
            return render_template('yesno.html', **locals())
        elif responce == 1:  # If DM send command 1, then there is no conflict, device changed, render main.html page
            # Taking status of devices, updating it
            statusLamp = check_status(395)
            statusKettle = check_status(19)
            smile = Markup("https://github.com/BiggyBaron/VirtualAssistant/blob/master/static/sucsses.gif?raw=true")
            return render_template('main.html', **locals())
    # Taking status of devices, updating it
    statusLamp = check_status(395)
    statusKettle = check_status(19)
    smile = Markup("https://github.com/BiggyBaron/VirtualAssistant/blob/master/static/hello.gif?raw=true")
    return render_template('main.html', **locals())


# YesNo page, where user decides go through the conflict or skip it and cancel order
@app.route("/<username>/<order>/yesno", methods=["GET", "POST"])  # Unique route of the page
def yesno(username, order):
    Info, header = readANS()  # Read data from answer.txt files and send it to render
    manual, mheader = readMan()  # Read data from manual.txt files and send it to render
    # Taking status of devices, updating it
    statusLamp = check_status(395)
    statusKettle = check_status(19)
    text = ''
    reason = "noreason"
    if request.method == 'POST':  # If user POST by clicking submit button any text
        text = request.form['text3']
        if text == "no" or text == "No" or text == "Nope":  # If answer is No then render main.html
            answer = "Okay, waiting for orders."
            # Taking status of devices, updating it
            statusLamp = check_status(395)
            statusKettle = check_status(19)
            smile = Markup("https://github.com/BiggyBaron/VirtualAssistant/blob/master/static/waiting.gif?raw=true")
            return render_template('main.html', **locals())
        else:  # Else then render reason.html page and ask about reason
            answer = "Please, define your reason."
            # Taking status of devices, updating it
            statusLamp = check_status(395)
            statusKettle = check_status(19)
            smile = Markup("https://github.com/BiggyBaron/VirtualAssistant/blob/master/static/reason.gif?raw=true")
            return render_template('reason.html', **locals())


# Reason classification page, here system asks user to give a reason for the order
@app.route("/<username>/<reason>/<order>", methods=["GET", "POST"])  # Unique route with data about username and etc.
def reasonClassification(username, order, reason):
    Info, header = readANS()  # Read data from answer.txt files and send it to render
    manual, mheader = readMan()  # Read data from manual.txt files and send it to render
    # Taking status of devices, updating it
    statusLamp = check_status(395)
    statusKettle = check_status(19)
    text = ''
    if request.method == 'POST':  # If user POST by clicking submit button any text
        text = request.form['text2']
        write2dbLOG("reasonraw", text)  # Writing to table raw version of reason
        # Taking status of devices, updating it
        statusLamp = check_status(395)
        statusKettle = check_status(19)
        try:
            answer, reason, smile, responce = DM.DMreason(text, username, order)  # Send to DM and ask render data
        except IndexError:  # If system did not managed to classify reason it asks again
            answer = "Sorry, I could not classify your reason. Please, try again with different phrase."
            smile = Markup("https://github.com/BiggyBaron/VirtualAssistant/blob/master/static/waiting.gif?raw=true")
            reason = "noreason"
            return render_template('reason.html', **locals())
        smile = Markup(smile)
        write2dbLOG("output", responce)  # It writes output of CBR to database
        write2dbLOG("reasondef", reason)  # It writes classified reason to database
        Info, header = Summary()  # Takes summary to show and renders page
    # Taking status of devices, updating it
    statusLamp = check_status(395)
    statusKettle = check_status(19)
    return render_template('summary.html', **locals())


# Main flask app
if __name__ == "__main__":
    # It creates https access by last argument. It is need to be give to web-page permission to microphone
    app.run(host='0.0.0.0', port=8090, ssl_context='adhoc')  # If no need in https, just delete last argument
