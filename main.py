import time as TTT

from flask import Flask, render_template, request, send_from_directory

import FUNCorder as f

app = Flask(__name__)


## Login page without pass
@app.route("/")
def login():
    return render_template(
        "login.html", **locals())


# TODO: make engine to change the politics conf file online
@app.route("/politics")
def pol():
    politic = "something is to be written"
    return render_template(
        "Politics.html", **locals())


# TODO: finish core processes inside the test.py and put it here
@app.route("/<username>", methods=['GET', 'POST'])
def chat(username):
    statusLamp = f.check_status(395)
    statusKettle = f.check_status(19)
    activities = f.activity()
    if request.method == 'POST':
        usertype = f.user_type(username)
        if usertype == 0:
            return "No users"
        text = request.form['text']
        if text.lower() == "yes":
            fuck = "Please, explain me: why you want to change device status?"
            return render_template('father.html', **locals())
        elif text.lower() == "no":
            fuck = "Okay, that is nice!"
            f.make_order(0, username)
            return render_template('father.html', **locals())
        elif f.check_order(username) == 0:
            f.make_order(1, username)
            order = f.class_order(text)
            if not order:
                fuck = "Sorry, I cannot classify the order"
                f.make_order(0, username)
                return render_template('father.html', **locals())
            elif f.check_same(order) == 1:
                fuck = "Device is already in your status"
                return render_template('father.html', **locals())
            pol = f.check_pol(order, usertype, 0)
            f.write_order(order, username)
            if pol == 0:
                fuck = str(f.Give_answer(order, usertype, "temp",
                                         username)) + "\n Do want me to write your order to Global Politics?"
                TTT.sleep(1)
                statusLamp = f.check_status(395)
                statusKettle = f.check_status(19)
                activities = f.activity()
                f.make_order(1, username)
                return render_template('father.html', **locals())
            elif pol == 9:
                f.make_order(0, username)
                fuck = "Sorry, but you cannot change the device status, because of Global Policy and you do not have enough priority level to change this Global Policy. Contact adult."
                return render_template('father.html', **locals())
            else:
                f.make_order(1, username)
                fuck = "Sorry, but you cannot change the device status, because of Global Policy. Do you want to try to change it anyway? Answer yes or not:"
                return render_template('father.html', **locals())
        else:
            f.make_order(0, username)
            reason = f.class_reason(text)
            if not reason:
                fuck = "Sorry, I cannot classify the reason"
                f.make_order(1, username)
                return render_template('father.html', **locals())
            order = f.write_order(0, username)
            pol = f.check_pol(order, usertype, reason)
            if pol == 0:
                order = f.write_order(0, username)
                fuck = f.Give_answer(order, usertype, reason, username)
                TTT.sleep(1)
                statusLamp = f.check_status(395)
                statusKettle = f.check_status(19)
                activities = f.activity()
                return render_template('father.html', **locals())
            else:
                fuck = "Sorry, but you do not have good reason."
                f.write_order(" ", username)
                return render_template('father.html', **locals())
    else:
        fuck = "Hello, " + str(username) + ", I am your Virtual Assistant. Type or say me your order."
    return render_template('father.html', **locals())


# TODO: create some logging engine
## Uploading logs, It is working
@app.route("/logs")
def log():
    return render_template(
        "logs.html", **locals())


@app.route('/logs/<filename>', methods=['GET'])
def return_file(filename):
    print(filename)
    return send_from_directory(directory='Conf', filename=filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090)
