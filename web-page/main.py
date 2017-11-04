from flask import Flask, flash, redirect, render_template, request, session, abort, send_from_directory

app = Flask(__name__)

## Login page without pass
@app.route("/")
def login():
    return render_template(
        "login.html", **locals())

@app.route("/politics")
def pol():
    politic = "something is to be written"
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

## Uploading logs, It is working
@app.route("/logs")
def log():
    return render_template(
        "logs.html", **locals())

@app.route('/logs/<filename>',methods=['GET'])
def return_file(filename):
    print(filename)
    return send_from_directory(directory='Conf', filename=filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090)
