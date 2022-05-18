from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def cantine():
    return render_template("main.html")