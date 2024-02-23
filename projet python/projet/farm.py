from flask import Flask,redirect, render_template
from flask import request
import json

app = Flask(__name__)


@app.route("/")
def index():
    farms = json.load(open('projet python\\gestion_taches_v01\\gestion_taches\\taches.json'))
    builders = json.load(open('projet python\\gestion_taches_v01\\gestion_taches\\employes.json'))
    return render_template('index.html', farms=farms, builders = builders)

@app.route("/farm/add", methods=['GET'])
def fadd():
    return render_template('addfarm.html')

@app.route("/farm/add", methods=['POST'])
def faddPOST():
    
    farms = json.load(open('projet python\\gestion_taches_v01\\gestion_taches\\taches.json'))

    # creation d'un nouveau todo
    newfarm =  {}
    newfarm['title'] = request.form['title']
    #gestin des employes assignes
    if (request.form.get['employee'] == json.load(open('projet python\\gestion_taches_v01\\gestion_taches\\employes.json'))):
        newfarm['employee'] = {request.form.get['employee']}
    else:
        newfarm['employee'] = None
    # la gestion du done est un peu plus compliquee...
    if(request.form.get('done')):
        newfarm['statut'] = 'done'
        newfarm['employee'] = None
    elif(request.form.get('in Progress')):    
        newfarm['statut'] = 'in Progress'
    else:
        newfarm['statut'] = 'unnasigned'
    newfarm['description'] = request.form.get['descrition']

    # on lui donne un id unique : le plus grand id + 1
    newfarm['id'] = (max(farms, key = lambda x: x['id'])['id'])+1
    farms.append(newfarm)

    # on ecrase le fichier avec la liste mise a jour
    json.dump(farms, open('projet python\\gestion_taches_v01\\gestion_taches\\taches.json', 'w'))

    return redirect('/todos')

@app.route("/farm/modify?<int:id>", methods=['GET'])

@app.route("/farm/modify?<int:id>", methods=['POST'])

@app.route("/farm/remove?<int:id>", methods=['GET'])

@app.route("/farm/remove?<int:id>", methods=['POST'])

@app.route("/farm/status?<int:id>", methods=['GET'])

@app.route("/farm/status?<int:id>", methods=['POST'])

@app.route("/builder/add", methods=['GET'])
def badd():
    return render_template('addbuilder.html')

@app.route("/builder/add", methods=['POST'])

@app.route("/builder/modify", methods=['GET'])

@app.route("/builder/modify", methods=['POST'])

@app.route("/builder/remove", methods=['GET'])

@app.route("/builder/remove", methods=['POST'])

@app.route("/builder/assign", methods=['GET'])

@app.route("/builder/assign", methods=['POST'])


app.run()
