from flask import Flask, flash, redirect, render_template, request, session, abort, send_from_directory
import FUNCorder as f

app = Flask(__name__)
f.make_order(0)

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
        elif text.lower() == "no":
            fuck = "Okay, that is nice!"
            f.make_order(0)
        elif f.check_order() == 0:
            f.make_order(1)
            order = f.class_order(text)
            if not order:
                fuck = "Sorry, I cannot classify the order"
                f.make_order(0)
                return render_template('father.html', **locals())
            pol = f.check_pol(order, usertype, 0)
            f.write_order(order)
            if pol == 0:
                fuck = f.Give_answer(order)
            elif pol == 9:
                f.make_order(0)
                fuck = "Sorry, but you cannot change the device status, because of Global Policy and you do not have enough priority level to change this Global Policy. Contact adult."
            else:
                fuck = "Sorry, but you cannot change the device status, because of Global Policy. Do you want to try to change it anyway? Answer yes or not:"
        else:
            f.make_order(0)
            reason = f.class_reason(text)
            if not reason:
                fuck = "Sorry, I cannot classify the reason"
                f.make_order(1)
                return render_template('father.html', **locals())
            order = f.write_order(0)
            pol = f.check_pol(order, usertype, reason)
            if pol == 0:
                order = f.write_order(0)
                f.write_order(" ")
                fuck = f.Give_answer(order)
            else:
                fuck = "Sorry, but you do not have good reason."
                f.write_order(" ")
    else:
        fuck = "Here will be answer"
    return render_template('father.html', **locals())


if __name__ == "__main__":
    app.run(host='192.168.1.1', port=8090)