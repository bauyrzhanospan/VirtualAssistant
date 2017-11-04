from flask import Flask, flash, redirect, render_template, request, session, abort

app = Flask(__name__)

@app.route("/")
def login():
    return render_template(
        "login.html", **locals())

@app.route("/politics")
def pol():
    return render_template(
        "Politics.html", **locals())

@app.route("/<username>", methods=['GET','POST'])
def chat(username):
    if request.method == 'POST':
        text = request.form['text']
        fuck = str(text.upper())
    else:
        fuck = "Here will be text"
    return render_template(
        'father.html', **locals())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090)
