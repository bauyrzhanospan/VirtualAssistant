import time as TTT
from flask import Flask, render_template, request, send_from_directory, abort
import FUNCorder as f
from Classification.classify import classifyR as classr
from Classification.classify import classifyO as classo

app = Flask(__name__)

## Login page without pass
@app.route("/")
def login():
    return render_template(
        "login.html", **locals())


@app.route("/<username>", method=['GET', 'POST'])
def user(username):
    # Default answer of the bot is greeting
    answer = str(username) + ", I am your Virtual Assistant. Type or say me your order."
    return render_template('father.html', **locals())


@app.route("/<username>/order", method=["GET", "POST"])
def orderClassification():
    text = ''
    if request.method == 'POST':
        text = request.form['text']
    order = classr(text)
    



@app.route("/<username>", methods=['GET', 'POST'])
def chat(username):
    # Checking usertype, if none = return error
    usertype = f.user_type(username)
    if usertype == 0:
        abort(404)

    # Checking device statuses (device number is located in official web-site of smart home)
    statusLamp = f.check_status(395)
    statusKettle = f.check_status(19)

    # Creating blocks with las activity data
    activities = f.activity()

    # Default answer of the bot is greeting
    answer = "Hello, " + str(username) + ", I am your Virtual Assistant. Type or say me your order."

    # Taking data from user:
    if request.method == 'POST':
        text = request.form['text']

        # If answer is @yes then redirect to the reason analyser page
        if text.lower() == "yes":
            answer = "Please, explain me: why you want to change device status? "
            return render_template('father.html', **locals())

        elif text.lower() == "no":
            answer = "Okay, that is nice!"
            f.make_order(0, username)
            return render_template('father.html', **locals())

        elif f.check_order(username) == 0:

            #
            f.make_order(1, username)

            # Classify the order, and if no order - speak:
            order = f.class_order(text)

            print(order)

            if not order:
                answer = str(f.answerme(text))
                return render_template('father.html', **locals())
            elif f.check_same(order) == 1:
                answer = "Device is already in the status that you wanted."
                return render_template('father.html', **locals())
            f.write_order(order, username)
            # Checking the orders list
            pol = f.check_pol(order, usertype, 0)

            # If there is no conflicting orders - than execute the order
            if pol == 0:

                # Change the status of the order and creating answer
                answer = str(f.Give_answer(order, usertype, "temp",
                                           username)) + ". Your order has no reason; as a result any other user with " \
                                                        "enough priority can eliminate your order. If you want to " \
                                                        "make the order permanent, you need to indicate the reason. " \
                                                        "Do you want to make it permanent? Answer yes or no, please."

                # Giving delay to new status been written to the Smart Home
                TTT.sleep(1)

                # Sync devices` statuses
                statusLamp = f.check_status(395)
                statusKettle = f.check_status(19)

                activities = f.activity()

                f.make_order(1, username)

                return render_template('father.html', **locals())

            # If there is policy and user has no enough priority:
            elif pol == 9:
                f.make_order(0, username)
                answer = "Sorry, but you cannot change the device status, because of Global Policy and you do not " \
                         "have enough priority level to change the device status. Contact user with higher priority. "
                return render_template('father.html', **locals())
            else:
                f.make_order(1, username)
                answer = "Sorry, but you cannot change the device status. Do you want to " \
                         "try to change it anyway? Answer yes or no: "
                return render_template('father.html', **locals())
        else:
            f.make_order(0, username)
            reason = f.class_reason(text)
            if not reason:
                answer = "Sorry, I cannot classify the reason"
                f.make_order(1, username)
                return render_template('father.html', **locals())
            order = f.write_order(0, username)
            pol = f.check_pol(order, usertype, reason)
            if pol == 0:
                order = f.write_order(0, username)
                answer = f.Give_answer(order, usertype, reason, username)
                TTT.sleep(1)
                statusLamp = f.check_status(395)
                statusKettle = f.check_status(19)
                activities = f.activity()
                return render_template('father.html', **locals())
            elif pol == 3:
                f.make_order(0, username)
                answer = "Sorry, your priority and reason are the same as other user`s. I cannot make any changes, " \
                         "because I have no enough legitimate power. "
                return render_template('father.html', **locals())
            else:
                answer = "Sorry, but you have no good reason."
                f.write_order(" ", username)
                return render_template('father.html', **locals())
    else:
        answer = "Hello, " + str(username) + ", I am your Virtual Assistant. Type or say me your order."
    return render_template('father.html', **locals())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090)
