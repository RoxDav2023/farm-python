from flask import Flask,redirect, render_template
from flask import request
import json

app = Flask(__name__)

#default route

@app.route("/")
def index():
    farms = json.load(open('projet python\\projet\\taches.json'))
    builders = json.load(open('projet python\\projet\\employes.json'))
    return render_template('index.html', farms=farms, builders = builders)

#Farms path

@app.route("/farm/add", methods=['GET'])
def farmAdd():
    return render_template('addfarm.html')

@app.route("/farm/add", methods=['POST'])
def farmAddPOST():
    
    farms = json.load(open('projet python\\projet\\taches.json'))
    builders = json.load(open('projet python\\projet\\employes.json'))
    addfarmtobuilder = {}

    # creation d'un nouveau todo
    newfarm =  {}
    newfarm['title'] = request.form['title']
    #gestion des employes assignes

    ## modification necessaire ##
    newfarm['employee'] = []

    if (request.form.get['employee'] == json.load(open('projet python\\projet\\employes.json'))):
        newfarm['employee'] = newfarm['employee'].append(request.form.get['employee'])

    # la gestion du done est un peu plus compliquee...
    if(request.form.get('done')):
        newfarm['statut'] = 'done'
        newfarm['employee'] = newfarm['employee'].clear()
    elif(request.form.get('in Progress')):    
        newfarm['statut'] = 'in Progress'
    else:
        newfarm['statut'] = 'unnasigned'
    newfarm['description'] = request.form.get['descrition']

    # on lui donne un id unique : le plus grand id + 1
    newfarm['id'] = (max(farms, key = lambda x: x['id'])['id'])+1
    farms.append(newfarm)

    # on ecrase le fichier avec la liste mise a jour
    json.dump(farms, open('projet python\\projet\\taches.json', 'w'))

    return redirect('/')

@app.route("/farm/modify?<int:id>", methods=['GET'])
def modifyFarm(id):
    print(id)
    farms = json.load(open('projet python\\projet\\taches.json'))

    farm = list(filter(lambda x: x['id'] == id, farms))[0]
    return render_template('modifyFarm.html', farm=farm)

@app.route("/farm/modify?<int:id>", methods=['POST'])
def modifyFarmPOST(id):
    farms = json.load(open('projet python\\projet\\taches.json'))

    farm = list(filter(lambda x:x['id'] == id, farms))[0]

    farm['title']=request.form['title']

    if(request.form.get('unnasigned')):
        farm['statut'] = 'unnasigned'
    elif(request.form.get('in Progress')):
        farm['statut'] = 'in Progress'
    else:
        farm['statut'] = 'unnasigned'

    json.dump(farms, open('projet python\\projet\\taches.json', 'w'))

    return redirect('/')

@app.route("/farm/remove?<int:id>", methods=['GET'])
def removeFarm(id):
    print(id)
    farms = json.load(open('projet python\\projet\\taches.json'))
    farms = list(filter(lambda x:x['id'] != id, farms))

    json.dump(farms, open('projet python\\projet\\taches.json', 'w'))

    return redirect('/')

@app.route("/farm/status?<int:id>")
def showstatus():
    farms = json.load(open('projet python\\projet\\taches.json'))

    return render_template('statusFarm.html', farms = farms)

#Builders path

@app.route("/builder/add", methods=['GET'])
def builderAdd():
    return render_template('addbuilder.html')

@app.route("/builder/add", methods=['POST'])
def builderAddPOST():    
    builders = json.load(open('projet python\\projet\\taches.json'))
    farms = json.load(open('projet python\\projet\\taches.json'))

    # creation d'un nouveau todo
    farms={}
    farms['title'] = request.form['assigned to']
    builder =  {}
    builder['lname'] = request.form['last name']
    builder['fname'] = request.form['first name']
    builder['gamertag'] = request.form['gamertag']
    builder['icon'] = request.form['icon']
    builder['assigned to'] = []
    #verifie si plus que trois
    if(len(builder['assigned to'])<3):
        builder['assigned to'] = builder['assigned to'].append(farms['title'])
    else:
        print("this builder can not be assigned to any more tasks for the moment, please finish the task or reassign this builder before giving hime more tasks")

    # on lui donne un id unique : le plus grand id + 1
    builder['id'] = (max(builders, key = lambda x: x['id'])['id'])+1
    builders.append(builder)

    # on ecrase le fichier avec la liste mise a jour
    json.dump(builders, open('projet python\\projet\\taches.json', 'w'))

    return redirect('/')

@app.route("/builder/modify?<int:id>", methods=['GET'])
def modifyBuilder(id):
    print(id)
    builders = json.load(open('projet python\\projet\\employes.json'))

    builder = list(filter(lambda x:x['id'] == id, builders))[0]
    return render_template('modifyBuilder.html', builder = builder)

@app.route("/builder/modify?<int:id>", methods=['POST'])
def modifyBuilderPOST(id):
    builders = json.load(open('projet python\\projet\\employes.json'))
    farms = json.load(open('projet python\\projet\\taches.json'))
    builder = list(filter(lambda x:x['id'] == id, builders))[0]
    farm={}
    farm['title'] = request.form['assigned to']
    builder['lname'] = request.form['last name']
    builder['fname'] = request.form['first name']
    builder['gamertag'] = request.form['gamertag']
    builder['icon'] = request.form['icon']
    builder['assigned to'].append(farms['title'])

    json.dump(builders, open('projet python\\projet\\employes.json', 'w'))
    return redirect('/')

@app.route("/builder/remove?<int:id>", methods=['GET'])
def removeBuilder(id):
    builders=json.load(open('projet python\\projet\\employes.json'))

    builders = list(filter(lambda x:x['id'] != id, builders))

    json.dump(builders, open('projet python\\projet\\employes.json', 'w'))

    return redirect('/')
@app.route("/builder/assign", methods=['GET'])
def assignBuilder(id):
    builders = json.load(open('projet python\\projet\\employes.json'))
    builder = list(filter(lambda x:x['id'] == id, builders))[0]

    return render_template('assignBuilder.html', builder = builder)

@app.route("/builder/assign", methods=['POST'])
def assignBilderPOST(id):
    builders = json.load(open('projet python\\projet\\employes.json'))
    builder = list(filter(lambda x:x['id'] == id, builders))[0]

    if builder['assigned to'] <3:
        builder['assigned to'].append(request.form['assigned to'])
    else:
        print('this builder cannot be assigned more tasks')
    
    json.dump(builders, open('projet python\\projet\\employes.json'))

    return redirect('/')
app.run(debug=True)
