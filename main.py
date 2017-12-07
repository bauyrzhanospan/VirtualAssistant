import time as TTT
from flask import Flask, render_template, request, Markup
import DM
import urllib
import random

app = Flask(__name__)


def check_status(deviceNum):
    data = urllib.request.urlopen("http://10.12.102.156/port_3480/data_request?id=lu_status").read()
    d = data.decode("utf-8")
    try:
        Status = int(d.split('"id": ' + str(deviceNum))[1].split('" }', 1)[0].strip()[-1])
        states = ["off", "on"]
        return states[Status]
    except:
        return "or not?"


def randomiser(cmd):
    if cmd == "user":
        users = ["Father", "Mother", "Son", "Grandpa"]
        usertypes = {"Father": "adult", "Mother": "adult", "Son": "young", "Grandpa": "older"}
        priorities = {"adult": "highest", "older": "second highest", "young": "lowest"}
        preferences = {"adult": "1: Security, 2: Health, 3: Work, 4: Food, 5: Energy, 6: Entertainment",
                       "older": "1: Health, 2: Security, 3: Work, 4: Food, 5: Energy, 6: Entertainment",
                       "young": "1: Security, 2: Work, 3: Entertainment, 4: Health, 5: Food, 6: Energy"}
        user = random.SystemRandom().choice(users)
        usertype = usertypes[user]
        priority = priorities[usertype]
        preference = preferences[usertype]
        answer = str(user) + "'.<br>" + str(user) + " is '" + str(usertype) + "' usertype which is the " \
                 + str(priority) + " priority usertype.<br>" + str(user) + " has next preferences:<br><br>" \
                 + str(preference)
    return answer


## Login page without pass
@app.route("/")
def login():
    header = "Welcome to the evaluation test"
    Info = "You are chosen to be the one who will test our new system.<br>Please, go through instructions. " \
           "<br><br><h4>Instruction:</h4><br>" \
           "Evaluation system is fully randomised with secure blind crypto randomizer.<br>And randomiser choose you " \
           "to be user '" + str(randomiser("user"))
    Info = Markup(Info)
    return render_template(
        "login.html", **locals())


@app.route("/<username>", methods=['GET', 'POST'])
@app.route("/<username>/<order>/", methods=["GET", "POST"])
def orderClassification(username, order="noorder"):
    statusLamp = check_status(395)
    statusKettle = check_status(19)
    text = ''
    answer = "Hello, " + str(username).title() + ", I am your Virtual Assistant. Type or say me your order."
    if request.method == 'POST':
        text = request.form['text']
        responce, answer, conflict, order = DM.DMorder(text, username)
        if responce == 0:
            statusLamp = check_status(395)
            statusKettle = check_status(19)
            smile = "./static/yesno.gif"
            return render_template('yesno.html', **locals())
        elif responce == 1:
            statusLamp = check_status(395)
            statusKettle = check_status(19)
            smile = "./static/sucssess.gif"
            return render_template('main.html', **locals())
    statusLamp = check_status(395)
    statusKettle = check_status(19)
    smile = "./static/hello.gif"
    return render_template('main.html', **locals())


@app.route("/<username>/<order>/yesno", methods=["GET", "POST"])
def yesno(username, order):
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
            smile = "./static/waiting.gif"
            return render_template('main.html', **locals())
        else:
            answer = "Please, define your reason."
            statusLamp = check_status(395)
            statusKettle = check_status(19)
            smile = "./static/reason.gif"
            return render_template('reason.html', **locals())


@app.route("/<username>/<reason>/<order>", methods=["GET", "POST"])
def reasonClassification(username, order, reason):
    statusLamp = check_status(395)
    statusKettle = check_status(19)
    text = ''
    if request.method == 'POST':
        text = request.form['text']
        statusLamp = check_status(395)
        statusKettle = check_status(19)
        answer, reason, smile = DM.DMreason(text, username, order)
    statusLamp = check_status(395)
    statusKettle = check_status(19)
    return render_template('main.html', **locals())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090, debug=True)
