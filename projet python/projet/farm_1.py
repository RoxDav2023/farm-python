from flask import Flask, redirect, render_template
from flask import request
import json

app = Flask(__name__)

# Default route
@app.route("/")
def index():
    farms = json.load(open('projet python\\projet\\taches.json'))
    builders = json.load(open('projet python\\projet\\employes.json'))
    return render_template('index.html', farms=farms, builders=builders)

# Farms path
@app.route("/farm/add", methods=['GET'])
def farmAdd():
    return render_template('addfarm.html')

@app.route("/farm/add", methods=['POST'])
def farmAddPOST():
    farms = json.load(open('projet python\\projet\\taches.json'))
    builders = json.load(open('projet python\\projet\\employes.json'))
    addfarmtobuilder = {}

    # Creation d'un nouveau todo
    newfarm =  {}
    newfarm['title'] = request.form['title']
    # Gestion des employes assignes
    ## Modification necessaire ##
    newfarm['employee'] = []

    if request.form.get('employee') in json.load(open('projet python\\projet\\employes.json')):
        newfarm['employee'].append(request.form.get('employee'))

    # La gestion du done est un peu plus compliquee...
    if request.form.get('done'):
        newfarm['statut'] = 'done'
        newfarm['employee'].clear()
    elif request.form.get('in Progress'):    
        newfarm['statut'] = 'in Progress'
    else:
        newfarm['statut'] = 'unnasigned'
    newfarm['description'] = request.form.get('description')

    # On lui donne un id unique : le plus grand id + 1
    newfarm['id'] = (max(farms, key=lambda x: x['id'])['id']) + 1
    farms.append(newfarm)

    # On ecrase le fichier avec la liste mise a jour
    json.dump(farms, open('projet python\\projet\\taches.json', 'w'))

    return redirect('/')

@app.route("/farm/modify/<int:id>", methods=['GET'])
def modifyFarm(id):
    farms = json.load(open('projet python\\projet\\taches.json'))
    farm = next((farm for farm in farms if farm['id'] == id), None)
    if farm:
        return render_template('fedit.html', farm=farm)
    else:
        return "Farm not found", 404

@app.route("/farm/modify/<int:id>", methods=['POST'])
def modifyFarmPOST(id):
    farms = json.load(open('projet python\\projet\\taches.json'))
    farm = next((farm for farm in farms if farm['id'] == id), None)
    if farm:
        farm['title'] = request.form['title']
        if request.form.get('done'):
            farm['statut'] = 'done'
            farm['employee'] = []
        elif request.form.get('in Progress'):
            farm['statut'] = 'in Progress'
        else:
            farm['statut'] = 'unnasigned'
        farm['description'] = request.form.get('description')

        json.dump(farms, open('projet python\\projet\\taches.json', 'w'))
        return redirect('/')
    else:
        return "Farm not found", 404

@app.route("/farm/remove/<int:id>", methods=['GET'])
def removeFarm(id):
    farms = json.load(open('projet python\\projet\\taches.json'))
    farms = [farm for farm in farms if farm['id'] != id]
    json.dump(farms, open('projet python\\projet\\taches.json', 'w'))
    return redirect('/')

@app.route("/farm/status/<int:id>", methods=['GET'])
def showstatus(id):
    farms = json.load(open('projet python\\projet\\taches.json'))
    farm = next((farm for farm in farms if farm['id'] == id), None)
    if farm:
        return render_template('fstatus.html', farm=farm)
    else:
        return "Farm not found", 404

#Builders Path
    
# Builders path
@app.route("/builder/add", methods=['GET'])
def builderAdd():
    return render_template('badd.html')

@app.route("/builder/add", methods=['POST'])
def builderAddPOST():
    builders = json.load(open('projet python\\projet\\employes.json'))
    farms = json.load(open('projet python\\projet\\taches.json'))

    builder = {}
    builder['lname'] = request.form['last name']
    builder['fname'] = request.form['first name']
    builder['gamertag'] = request.form['gamertag']
    builder['icon'] = request.form['icon']
    builder['assigned_to'] = []

    if len(builder['assigned_to']) < 3:
        builder['assigned_to'].append(request.form['assigned_to'])
        builders.append(builder)
        json.dump(builders, open('projet python\\projet\\employes.json', 'w'))
        return redirect('/')
    else:
        return "This builder cannot be assigned more tasks", 400

@app.route("/builder/modify/<int:id>", methods=['GET'])
def modifyBuilder(id):
    builders = json.load(open('projet python\\projet\\employes.json'))
    builder = next((builder for builder in builders if builder['id'] == id), None)
    if builder:
        return render_template('bedit.html', builder=builder)
    else:
        return "Builder not found", 404

@app.route("/builder/modify/<int:id>", methods=['POST'])
def modifyBuilderPOST(id):
    builders = json.load(open('projet python\\projet\\employes.json'))
    builder = next((builder for builder in builders if builder['id'] == id), None)
    if builder:
        builder['lname'] = request.form['last name']
        builder['fname'] = request.form['first name']
        builder['gamertag'] = request.form['gamertag']
        builder['icon'] = request.form['icon']

        json.dump(builders, open('projet python\\projet\\employes.json', 'w'))
        return redirect('/')
    else:
        return "Builder not found", 404

@app.route("/builder/assign/<int:id>", methods=['GET'])
def assignBuilder(id):
    builders = json.load(open('projet python\\projet\\employes.json'))
    builder = next((builder for builder in builders if builder['id'] == id), None)
    if builder:
        return render_template('bassign.html', builder=builder)
    else:
        return "Builder not found", 404

@app.route("/builder/assign/<int:id>", methods=['POST'])
def assignBuilderPOST(id):
    builders = json.load(open('projet python\\projet\\employes.json'))
    builder = next((builder for builder in builders if builder['id'] == id), None)
    if builder:
        if len(builder['assigned_to']) < 3:
            builder['assigned_to'].append(request.form['assigned_to'])
            json.dump(builders, open('projet python\\projet\\employes.json', 'w'))
            return redirect('/')
        else:
            return "This builder cannot be assigned more tasks", 400
    else:
        return "Builder not found", 404

@app.route("/builder/remove/<int:id>", methods=['GET'])
def removeBuilder(id):
    builders = json.load(open('projet python\\projet\\employes.json'))
    builders = [builder for builder in builders if builder['id'] != id]
    json.dump(builders, open('projet python\\projet\\employes.json', 'w'))
    return redirect('/')

app.run(debug=True)