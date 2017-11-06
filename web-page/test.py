import FUNCorder as f
from flask import Flask, render_template, request

app = Flask(__name__)
f.make_order(0, "father")
f.make_order(0, "mother")
f.make_order(0, "son")
f.make_order(0, "grandpa")

## Login page without pass
@app.route("/<username>", methods=['GET','POST'])
def login(username):

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
            pol = f.check_pol(order, usertype, 0)
            f.write_order(order, username)
            if pol == 0:
                fuck = str(f.Give_answer(order, usertype, "temp",
                                         username)) + "\n Do want me to write your order to Global Politics?"
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
                return render_template('father.html', **locals())
            else:
                fuck = "Sorry, but you do not have good reason."
                f.write_order(" ", username)
                return render_template('father.html', **locals())
    else:
        fuck = "Here will be answer"
    return render_template('father.html', **locals())


if __name__ == "__main__":
    app.run(host='localhost', port=8090)
