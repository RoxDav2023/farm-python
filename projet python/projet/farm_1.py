from flask import Flask, redirect, render_template
from flask import request
import json
import os

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
    return render_template('fadd.html')

@app.route("/farm/add", methods=['POST'])
def farmAddPOST():
    farms = json.load(open('projet python\\projet\\taches.json'))
    builders = json.load(open('projet python\\projet\\employes.json'))
    addfarmtobuilder = {}

    # Creation d'un nouveau todo
    newfarm =  {}
    newfarm['title'] = request.form['title']
    # Gestion des employes assignes
    
    newfarm['employee'] = []

    if request.form.get('employee') in json.load(open('projet python\\projet\\employes.json')):
        newfarm['employee'].append(request.form.get('employee'))

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
    json.dump(farms, open('projet python\\projet\\taches.json', 'w'), indent=4)

    return redirect('/')

@app.route("/farm/modify/<int:id>", methods=['GET'])
def modifyFarm(id):
    farms = json.load(open('projet python\\projet\\taches.json'))
    builders = json.load(open('projet python\\projet\\employes.json'))
    farm = next((farm for farm in farms if farm['id'] == id), None)
    if farm:
        return render_template('fedit.html', farm=farm, builders=builders)
    else:
        return "Farm not found"

@app.route("/farm/modify/<int:id>", methods=['POST'])
def modifyFarmPOST(id):
    farms = json.load(open('projet python\\projet\\taches.json'))
    builders = json.load(open('projet python\\projet\\employes.json'))
    farm = next((farm for farm in farms if farm['id'] == id), None)

    farm['title'] = request.form['title']
    farm['description'] = request.form.get('description')
    
    new_builder_id = request.form.get('builder')
    if new_builder_id:
        new_builder_id = int(new_builder_id)
        if farm['employee'] is None:
            farm['employee'] = []
        if new_builder_id not in farm['employee']:
            farm['employee'].append(new_builder_id)
    else:
        farm['employee'] = []
    
    status = request.form.get('status')
    if status == 'Unassigned':
        farm['statut'] = 'Unassigned'
        farm['employee'] = []  # Clear assigned builders when Unassigned
        # Remove farm ID from assigned_to field of all builders
        for builder in builders:
            if farm['id'] in builder.get('assigned_to', []):
                builder['assigned_to'].remove(farm['id'])
    elif status == 'Done':
        farm['statut'] = 'Done'
        farm['employee'] = []  # Clear assigned builders when Done
        # Remove farm ID from assigned_to field of all builders
        for builder in builders:
            if farm['id'] in builder.get('assigned_to', []):
                builder['assigned_to'].remove(farm['id'])
    elif status == 'In Progress':
        farm['statut'] = 'In Progress'
        in_progress_id = request.form.get('builder')
        if in_progress_id:
            in_progress_id = int(in_progress_id)
            previous_builder_id = farm.get('employee')
            farm['employee'] = [in_progress_id]
            
            # Remove farm ID from assigned_to field of previous builder
            
            previous_builder = next((builder for builder in builders if builder['id'] == previous_builder_id), None)
                
            if farm['id'] in previous_builder.get('assigned_to', []):
                previous_builder['assigned_to'].remove(farm['id'])
            
            # Update builder's assigned farms list with the farm ID in progress
            builder = next((builder for builder in builders if builder['id'] == in_progress_id), None)

            if 'assigned_to' not in builder:
                builder['assigned_to'] = []
            builder['assigned_to'].append(farm['id'])
        else:
            farm['employee'] = []  # Clear assigned builders when In Progress
            # Remove farm ID from assigned_to field of all builders
            for builder in builders:
                if farm['id'] in builder.get('assigned_to', []):
                    builder['assigned_to'].remove(farm['id'])

    with open('projet python\\projet\\taches.json', 'w') as f:
        json.dump(farms, f, indent=4)
    
    with open('projet python\\projet\\employes.json', 'w') as f:
        json.dump(builders, f, indent=4)
    
    return redirect('/')








@app.route("/farm/remove/<int:id>", methods=['GET'])
def removeFarm(id):
    farms = json.load(open('projet python\\projet\\taches.json'))
    farms = [farm for farm in farms if farm['id'] != id]
    json.dump(farms, open('projet python\\projet\\taches.json', 'w'), indent=4)
    return redirect('/')

@app.route("/farm/status/<int:id>", methods=['GET'])
def showstatus(id):
    farms = json.load(open('projet python\\projet\\taches.json'))
    farm = next((farm for farm in farms if farm['id'] == id), None)
    if farm:
        return render_template('fstatus.html', farm=farm)
    else:
        return "Farm not found"

#Builders Path
    
# Builders path
@app.route("/builder/add", methods=['GET'])
def builderAdd():
    farms = json.load(open('projet python\\projet\\taches.json'))
    for farm in farms:
        print(farm)  # Print each farm dictionary for debugging
    return render_template('badd.html', farms=farms)

@app.route("/builder/add", methods=['POST'])
def builderAddPOST():
    builders = json.load(open('projet python\\projet\\employes.json'))
    farms = json.load(open('projet python\\projet\\taches.json'))

    builder = {}
    builder['lname'] = request.form['last_name']
    builder['fname'] = request.form['first_name']
    builder['gamertag'] = request.form['gamertag']
    # builder['icon'] = request.form['icon']
    
    # Handle file upload
    if 'icon' in request.files:
        icon = request.files['icon']
        if icon.filename != '':
            image_dir = 'projet python\\projet\\image'
            os.makedirs(image_dir, exist_ok=True)
            icon_path = os.path.join(image_dir, icon.filename)
            icon.save(icon_path)
            builder['icon'] = icon_path
    else:
        builder['icon'] = None
    
    builder['id'] = (max(builders, key = lambda x: x['id'])['id'])+1

    builder['assigned_to'] = request.form.getlist('assigned_to')


    if len(builder['assigned_to']) < 3:
        builders.append(builder)
        json.dump(builders, open('projet python\\projet\\employes.json', 'w'), indent=4)
        return redirect('/')
    else:
        return "This builder cannot be assigned more tasks"

@app.route("/builder/modify/<int:id>", methods=['GET'])
def modifyBuilder(id):
    builders = json.load(open('projet python\\projet\\employes.json'))
    builder = next((builder for builder in builders if builder['id'] == id), None)
    return render_template('bedit.html', builder=builder)

@app.route("/builder/modify/<int:id>", methods=['POST'])
def modifyBuilderPOST(id):
    builders = json.load(open('projet python\\projet\\employes.json'))
    builder = next((builder for builder in builders if builder['id'] == id), None)
    
    builder['lname'] = request.form['last_name']
    builder['fname'] = request.form['first_name']
    builder['gamertag'] = request.form['gamertag']
    builder['icon'] = request.form['icon']

    json.dump(builders, open('projet python\\projet\\employes.json', 'w'), indent=4)
    return redirect('/')


@app.route("/builder/assign/<int:id>", methods=['GET'])
def assignBuilder(id):
    builders = json.load(open('projet python\\projet\\employes.json'))
    farms = json.load(open('projet python\\projet\\taches.json'))
    builder = next((builder for builder in builders if builder['id'] == id), None)

    return render_template('bassign.html', builder=builder, farms=farms)



@app.route("/builder/assign/<int:id>", methods=['POST'])
def assignBuilderPOST(id):
    builders = json.load(open('projet python\\projet\\employes.json'))
    farms = json.load(open('projet python\\projet\\taches.json'))
    builder = next((builder for builder in builders if builder['id'] == id), None)
    
    farm_name = request.form['farm']  # Get the selected farm name from the form

        # Find the farm by its name
    assigned_farm = next((farm for farm in farms if farm.get('title') == farm_name), None)
    
    # Update the farm's employee field with the builder's ID
    assigned_farm['employee'].append(builder['id'])
    
    # Add farm ID to the builder's assigned farms list
    if 'assigned_to' not in builder:
        builder['assigned_to'] = []
    builder['assigned_to'].append(assigned_farm['id'])

    # Save the updated farms list back to the taches.json file
    with open('projet python\\projet\\taches.json', 'w') as t:
        json.dump(farms, t, indent=4)

    # Save the updated builders list back to the employes.json file
    with open('projet python\\projet\\employes.json', 'w') as e:
        json.dump(builders, e, indent=4)

    return redirect('/')  # Redirect to the home page after assigning the farm


@app.route("/builder/remove/<int:id>", methods=['GET'])
def removeBuilder(id):
    builders = json.load(open('projet python\\projet\\employes.json'))
    builders = [builder for builder in builders if builder['id'] != id]
    json.dump(builders, open('projet python\\projet\\employes.json', 'w'), indent=4)
    return redirect('/')

app.run(debug=True)