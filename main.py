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
        return "somehow?"


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
    users2 = users
    users2.remove(u)
    u2 = random.SystemRandom().choice(users2)
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
    id23 = cur.execute("SELECT * FROM `eval` ORDER BY `eval`.`id` ASC LIMIT 10000")
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
    Manual = "<ol><li>On the login page choose '" + str(u) + "'. </li>" + \
             "<li>Then type or say (by clicking the microphone) in your own words the order to turn " \
             + str(["on", "off"][status]) + " the " + str(dev) + ".</li>" \
             + "<li>Then the system will inform you that there is a conflict and will ask you about " \
               "the next step. Type or say 'yes'." + "</li>" \
             + "<li>Then type or say (by clicking the microphone) in your own words the reason about the " + \
             str(Newreason) + " issue.</li>" + "<li>Then the system resolves the conflict and " \
                                               "you will need to answer the questionnaire." \
                                               "</li></ol>"
    summary = "<h2>Story:</h2><ol><li>Your user is " + str(u) + ", " + str(user) + " usertype (" + str(priority) + \
              " priority) with next preferences:<br>" + str(preference) + "<br></li><li>" + \
              "Other user is " + str(u2) + ", " + str(user2) + " usertype (" + str(priority2) + \
              " priority) with next preferences:<br>" + str(preference2) + "<br></li><li>" + \
              "Conflict: you (" + str(u) + ":" + str(user) + ") want to turn the " + str(dev) + \
              " " + str(["on", "off"][status]) + \
              " but other user (" + str(u2) + ":" + str(user2) + ") did the opposite. </li><li>" + \
              "Your (" + str(u2) + ", " + str(user2) + ") reason is: " + str(Newreason).upper() + \
              "</li><li>Other user`s (" + str(u2) + ", " + str(user2) + ") reason is " + str(reason).upper() + "</li>"
    with open("answer.txt", 'w') as out:
        out.write(answer)
    with open("manual.txt", 'w') as o:
        o.write(Manual)
    with open("summary.txt", 'w') as o:
        o.write(summary)


def Summary():
    header = "Summary"
    with open("summary.txt", 'r') as out:
        summary = out.read()
    con = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user=None, passwd=None, db='virtass')
    cur = con.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM `eval`')
    dataset = cur.fetchall()
    cur.close()
    con.close()
    print(dataset)
    orderraw = dataset[-1]["orderraw"]
    orderdef = dataset[-1]["orderdef"]
    reasonraw = dataset[-1]["reasonraw"]
    reasondef = dataset[-1]["reasondef"]
    output = dataset[-1]["output"]
    winner = [" other user`s ", " your "][output]
    summary = summary + "<li>System desided that" + str(winner) + \
              "order has a higher priority.</li></ol><h2>Classification:</h2><ol><li>Your order was: " + \
              str(orderraw) + "</li><li>System classified order as: " + str(orderdef) + "</li><li>" + \
              "Your reason was: " + str(reasonraw) + "</li><li>" + \
              "System classified reason as: " + str(reasondef) + "</li></ol>"
    answer = Markup(summary)
    return answer, header


def readANS():
    with open("answer.txt", 'r') as out:
        answer = out.read()
    Info = Markup(answer)
    header = "Welcome to the evaluation test"
    return Info, header


def readMan():
    with open("manual.txt", 'r') as out:
        answer = out.read()
    Info = Markup(answer)
    header = "Manual"
    return Info, header


## Login page without pass
@app.route("/")
def login():
    randomiser()
    Info, header = readANS()
    manual, mheader = readMan()
    return render_template(
        "login.html", **locals())


@app.route("/<username>", methods=['GET', 'POST'])
@app.route("/<username>/<order>/", methods=["GET", "POST"])
def orderClassification(username, order="noorder"):
    Info, header = readANS()
    manual, mheader = readMan()
    statusLamp = check_status(395)
    statusKettle = check_status(19)
    text = ''
    answer = "Hello, " + str(username).title() + ", I am your Virtual Assistant. Type or tell me your order."
    if request.method == 'POST':
        text = request.form['text']
        write2dbLOG("orderraw", text)
        try:
            responce, answer, conflict, order = DM.DMorder(text, username)
        except IndexError:
            answer = "Sorry, I could not classify your order. Please, try again with different phrase."
            smile = Markup("https://github.com/BiggyBaron/VirtualAssistant/blob/master/static/waiting.gif?raw=true")
            order = "noorder"
            return render_template('main.html', **locals())
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
    manual, mheader = readMan()
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
    manual, mheader = readMan()
    statusLamp = check_status(395)
    statusKettle = check_status(19)
    text = ''
    if request.method == 'POST':
        text = request.form['text']
        write2dbLOG("reasonraw", text)
        statusLamp = check_status(395)
        statusKettle = check_status(19)
        try:
            answer, reason, smile, responce = DM.DMreason(text, username, order)
        except IndexError:
            answer = "Sorry, I could not classify your reason. Please, try again with different phrase."
            smile = Markup("https://github.com/BiggyBaron/VirtualAssistant/blob/master/static/waiting.gif?raw=true")
            reason = "noreason"
            return render_template('reason.html', **locals())
        smile = Markup(smile)
        write2dbLOG("output", responce)
        write2dbLOG("reasondef", reason)
        Info, header = Summary()
    statusLamp = check_status(395)
    statusKettle = check_status(19)
    return render_template('summary.html', **locals())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090, debug=True)
