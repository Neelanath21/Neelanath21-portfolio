from flask import Flask, render_template

app = Flask('app')


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/exp')
def exp():
    return render_template("exp.html")


@app.route('/edu')
def edu():
    return render_template("edu.html")


@app.route('/pro')
def pro():
    return render_template("pro.html")


@app.route('/skl')
def skl():
    return render_template("skl.html")


app.run(host='0.0.0.0', port=8080)
