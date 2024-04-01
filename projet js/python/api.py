import requests

# Votre clé API Spoonacular
api_key = '6de7304103c9471ea3d59b2931dd2911'

# Les ingrédients que vous avez
ingredients = 'pommes, farine, sucre'

# Nombre maximum de recettes à retourner
number_of_recipes = 10

# Construisez l'URL de la requête
url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number={number_of_recipes}&apiKey={api_key}"

# Faites la requête GET
response = requests.get(url)

# Vérifiez si la requête a réussi
if response.status_code == 200:
    # Parsez la réponse JSON
    recipes = response.json()
    for recipe in recipes:
        print(recipe['title'])
else:
    print('Erreur dans la requête API')