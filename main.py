import time as TTT
from flask import Flask, render_template, request, Markup
import DM
import urllib
import random
import pymysql


app = Flask(__name__)


def write2dbLOG(key, value):
    con = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user=None, passwd=None, db='virtass')
    cur = con.cursor(pymysql.cursors.DictCursor)
    id = cur.execute("SELECT * FROM `eval` ORDER BY `eval`.`id` ASC LIMIT 10000")
    cur.execute("UPDATE `eval` SET `" + str(key) + "` = '" + str(value) + "' WHERE `eval`.`id` = '" + str(id) + "';")
    print(id)
    print("Key is " + str(key) + " and value is " + str(value))
    con.commit()
    cur.close()
    con.close()


def check_status(deviceNum):
    data = urllib.request.urlopen("http://10.12.102.156/port_3480/data_request?id=lu_status").read()
    d = data.decode("utf-8")
    try:
        Status = int(d.split('"id": ' + str(deviceNum))[1].split('" }', 1)[0].strip()[-1])
        states = ["off", "on"]
        return states[Status]
    except:
        return "or not?"


def randomiser():
    # Change rules table
    con = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user=None, passwd=None, db='virtass')
    cur = con.cursor(pymysql.cursors.DictCursor)
    users = ["Father", "Mother", "Son", "Grandpa"]
    usertypes2 = {"Father": "adult", "Mother": "adult", "Son": "young", "Grandpa": "elder"}
    reasons = ["energy", "entertainment", "food", "health", "security", "work"]
    devices = ["kettle", "lamp"]
    u = random.SystemRandom().choice(users)
    user = usertypes2[u]
    u2 = random.SystemRandom().choice(users)
    user2 = usertypes2[u2]
    reason = random.SystemRandom().choice(reasons)
    dev = random.SystemRandom().choice(devices)
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
    cur.execute("UPDATE `rules` SET `user` = '" + str(user2) + "' WHERE `rules`.`id` = 0")
    con.commit()
    cur.execute("UPDATE `rules` SET `reason` = '" + str(reason) + "' WHERE `rules`.`id` = 0")
    con.commit()
    cur.execute("UPDATE `rules` SET `device` = '" + str(dev) + "' WHERE `rules`.`id` = 0")
    con.commit()
    cur.execute("UPDATE `rules` SET `status` = '" + str(status) + "' WHERE `rules`.`id` = 0")
    con.commit()
    cur.close()
    con.close()

    # Add values to eval table
    con = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user=None, passwd=None, db='virtass')
    cur = con.cursor(pymysql.cursors.DictCursor)
    order = dev.title() + ["On", "Off"][status]
    Newreason = random.SystemRandom().choice(reasons)
    cur.execute("INSERT INTO `eval` (`user`, `otheruser`, `ordertype`, `rulereason`, `reason`) VALUES ('" +
                str(user) + "', '" + str(user2) + "', '" + str(order) + "', '" + str(reason) + "', '" + str(
        Newreason) + "');")
    con.commit()
    cur.close()
    con.close()

    # Write to answer
    priorities = {"adult": "highest", "elder": "second highest", "young": "lowest"}
    preferences = {"adult": "1: Security, 2: Health, 3: Work, 4: Food, 5: Energy, 6: Entertainment",
                   "elder": "1: Health, 2: Security, 3: Work, 4: Food, 5: Energy, 6: Entertainment",
                   "young": "1: Security, 2: Work, 3: Entertainment, 4: Health, 5: Food, 6: Energy"}
    priority = priorities[user]
    preference = preferences[user]
    priority2 = priorities[user2]
    preference2 = preferences[user2]

    answer = "You are chosen to be the one who will test our new system.<br>Please, go through instructions. " \
             "<br><br><h4>Instruction:</h4><br>" \
             "Evaluation system is fully randomised with secure blind crypto randomizer.<br>And randomiser choose you " \
             "to be user '"
    answer = answer + str(u) + "'.<br>" + str(u) + " is '" + str(user) + "' usertype which is the " \
             + str(priority) + " priority usertype.<br>" + str(u) + " has next preferences:<br><br>" \
             + str(preference) + "<br>"

    answer = answer + "<br>Other user of the system is '" + str(u2) + "' with usertype '" + str(
        user2) + "' which is the " \
             + str(priority2) + " priority usertype.<br>" + str(u2) + " has next preferences:<br><br>" \
             + str(preference2) + "<br><br>" + "<h5>Conflict:</h5><br>There is conflict between you and other " \
                                               "user.<br>Other user turned the " + str(dev) + " " + \
             str(["off", "on"][status]) + " with reason based on the " + str(reason) + " issue.<br>" + \
             "But you need the device to be in an opposite status because your reason is " + str(Newreason) \
             + " issue.<br> Let`s check how system will resolve this conflict. <br><h3>Manual</h3><br>" + \
             "<ol><li>At the login page choose '" + str(u) + "'. </li>" + \
             "<li>Then type or say (by clicking the microphone) order with your own words to turn " \
             + str(["on", "off"][status]) + " the " + str(dev) + ".</li>" \
             + "<li>Then the system will inform you that there is a conflict and asks you about " \
               "next step. Type or say 'yes'." + "</li>" \
             + "<li>Then type or say (by clicking the microphone) reason with your own words about " + \
             str(Newreason) + " issue.</li>" + "<li>Then system resolves conflict and you need to answer the questions." \
                                               "</li></ol>"
    with open("answer.txt", 'w') as out:
        out.write(answer)


def readANS():
    with open("answer.txt", 'r') as out:
        answer = out.read()
    Info = Markup(answer)
    header = "Welcome to the evaluation test"
    return Info, header


## Login page without pass
@app.route("/")
def login():
    randomiser()
    Info, header = readANS()
    return render_template(
        "login.html", **locals())


@app.route("/<username>", methods=['GET', 'POST'])
@app.route("/<username>/<order>/", methods=["GET", "POST"])
def orderClassification(username, order="noorder"):
    Info, header = readANS()
    statusLamp = check_status(395)
    statusKettle = check_status(19)
    text = ''
    answer = "Hello, " + str(username).title() + ", I am your Virtual Assistant. Type or say me your order."
    if request.method == 'POST':
        text = request.form['text']
        write2dbLOG("orderraw", text)
        responce, answer, conflict, order = DM.DMorder(text, username)
        write2dbLOG("orderdef", order)
        if responce == 0:
            statusLamp = check_status(395)
            statusKettle = check_status(19)
            smile = Markup("https://github.com/BiggyBaron/VirtualAssistant/blob/master/static/yesno.gif?raw=true")
            return render_template('yesno.html', **locals())
        elif responce == 1:
            statusLamp = check_status(395)
            statusKettle = check_status(19)
            smile = Markup("https://github.com/BiggyBaron/VirtualAssistant/blob/master/static/sucsses.gif?raw=true")
            return render_template('main.html', **locals())
    statusLamp = check_status(395)
    statusKettle = check_status(19)
    smile = Markup("https://github.com/BiggyBaron/VirtualAssistant/blob/master/static/hello.gif?raw=true")
    return render_template('main.html', **locals())


@app.route("/<username>/<order>/yesno", methods=["GET", "POST"])
def yesno(username, order):
    Info, header = readANS()
    statusLamp = check_status(395)
    statusKettle = check_status(19)
    text = ''
    reason = "noreason"
    if request.method == 'POST':
        text = request.form['text']
        if text == "no" or text == "No" or text == "Nope":
            answer = "Okay, waiting for orders."
            statusLamp = check_status(395)
            statusKettle = check_status(19)
            smile = Markup("https://github.com/BiggyBaron/VirtualAssistant/blob/master/static/waiting.gif?raw=true")
            return render_template('main.html', **locals())
        else:
            answer = "Please, define your reason."
            statusLamp = check_status(395)
            statusKettle = check_status(19)
            smile = Markup("https://github.com/BiggyBaron/VirtualAssistant/blob/master/static/reason.gif?raw=true")
            return render_template('reason.html', **locals())


@app.route("/<username>/<reason>/<order>", methods=["GET", "POST"])
def reasonClassification(username, order, reason):
    Info, header = readANS()
    statusLamp = check_status(395)
    statusKettle = check_status(19)
    text = ''
    if request.method == 'POST':
        text = request.form['text']
        write2dbLOG("reasonraw", text)
        statusLamp = check_status(395)
        statusKettle = check_status(19)
        answer, reason, smile, responce = DM.DMreason(text, username, order)
        smile = Markup(smile)
        write2dbLOG("output", responce)
        write2dbLOG("reasondef", reason)
    statusLamp = check_status(395)
    statusKettle = check_status(19)
    return render_template('main.html', **locals())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090, debug=True)
