from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/farm/add")

@app.route("/farm/modify")

@app.route("/farm/remove")

@app.route("/farm/status")

@app.route("/builder/add")

@app.route("/builder/modify")

@app.route("/builder/remove")

@app.route("/builder/assign")


app.run()
