from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route("/")
def index():
    farms = json.load(open('projet python\\gestion_taches_v01\\gestion_taches\\taches.json'))
    return render_template('index.html', farms=farms)

@app.route("/farm/add", methods=['GET'])

@app.route("/farm/add", methods=['POST'])

@app.route("/farm/modify?<int:id>", methods=['GET'])

@app.route("/farm/modify?<int:id>", methods=['POST'])

@app.route("/farm/remove?<int:id>", methods=['GET'])

@app.route("/farm/remove?<int:id>", methods=['POST'])

@app.route("/farm/status?<int:id>", methods=['GET'])

@app.route("/farm/status?<int:id>", methods=['POST'])

@app.route("/builder/add", methods=['GET'])

@app.route("/builder/add", methods=['POST'])

@app.route("/builder/modify", methods=['GET'])

@app.route("/builder/modify", methods=['POST'])

@app.route("/builder/remove", methods=['GET'])

@app.route("/builder/remove", methods=['POST'])

@app.route("/builder/assign", methods=['GET'])

@app.route("/builder/assign", methods=['POST'])


app.run()
