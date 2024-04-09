// function name1() {
//     var name = document.getElementById("nom").value;
//     window.alert("Bonjour " + name + " !");
//     console.log(name);
// }
function name1() {
    event.preventDefault(); // Pour éviter que le formulaire ne soit soumis et que la page ne soit rechargée
    var name = document.getElementById("nom").value;
    var greetingMessage = document.getElementById("greetingMessage");
    greetingMessage.textContent = "Bonjour " + name + "!";
    greetingMessage.style.display = "block"; // Pour afficher le message
    var form = document.getElementById("name");
    form.style.display = "none"; // Pour cacher le formulaire
}


function hideFormAndShowNext() {
    var form = document.getElementById("name");
    var next = document.getElementById("next1");
    var nextButton = document.getElementById("boutonnext1");
    var okButton = document.getElementById("boutonOk");

    form.style.display = "none"; // Pour cacher le formulaire
    next.style.display = "block"; // Pour afficher le paragraphe suivant
    nextButton.style.display = "none"; // Pour cacher le bouton "Next"
    okButton.style.display = "block"; // Pour afficher le bouton "Ok"
}

document.addEventListener("DOMContentLoaded", function() {
// meal generator //
const get_meal_btn = document.getElementById("get_meal");
const meal_container = document.getElementById("meal");

get_meal_btn.addEventListener('click', () => {
	fetch('https://www.themealdb.com/api/json/v1/1/random.php')
		.then(res => res.json())
		.then(res => {
			createMeal(res.meals[0]);
		})
		.catch(e => {
			console.warn(e);
		});
});


// create meal function

const createMeal = meal => {
    const ingredients = [];

    // obtenir tous les ingredients de l'objet. Jusqu'a 20.
    for (let i = 1; 1<= 20; i++) {
        if (meal["strIngredient${i}"]) {
            ingredients.push(
                `${meal["strIngredient${i}"]} - ${meal["strMeasure${i}"]}`
            );
        } else {
            // arret s'il n'a plus d'ingredients
            break;
        }
    }

    // get JSON response, parse and transform into HTML component //
    const newInnerHTML = `
        <div class="row">
            <div class="columns five">
                <img src="${meal.strMealThumb}" alt="Image Repas">
                ${
                    meal.strCategory
                    ? `<p><strong>Categorie:</strong> ${meal.strCategory}</p>`
                    : ""
                }
                $${meal.strArea ? `<p><strong>Area:</strong> ${meal.strArea}</p>` : " "}
                ${
                    meal.strTags
                        ?`<p><strong>Tags:</strong> ${meal.strTags
                            .split(",")
                            .join(", ")}</p>`
                        : ""
                }
                <h5>Ingredients:</h5>
                <ul>
                    ${ingredients.map(ingredient => `<li>${ingredient}</li>`).join("")}
                </ul>
            </div>
            ${
                meal.strYoutube
                    ? `
            <div class="row">
                <h5>Video recette</h5>
                <div class="videoWrapper">
                    <iframe width="420" height="315"
                    src="https://www.youtube.com/embed/${meal.strYoutube.slice(-11)}"
                    </iframe>
                </div>
            </div>`
                : ""
            }
        `;

        meal_container.innerHTML = newInnerHTML;
};
});





//api refrigerateur//

document.getElementById('validateBtn').addEventListener('click', function() {
    // Récupérer les choix sélectionnés
    const selectedChoices = document.querySelectorAll('input[type="checkbox"]:checked');
    const selectedValues = Array.from(selectedChoices).map(choice => choice.value);
    
    // Envoyer les choix à l'API
    fetch('url_de_votre_api', {
        method: 'POST', // ou 'GET' si nécessaire
        headers: {
            'Content-Type': 'application/json',
            // Ajoutez d'autres en-têtes si nécessaire
        },
        body: JSON.stringify({ filters: selectedValues }),
    })
    .then(response => {
        // Gérer la réponse de l'API ici
    })
    .catch(error => {
        console.error('Erreur lors de l\'envoi des données à l\'API :', error);
    });
});


// myfridge.html //
        document.getElementById('submitBtn').addEventListener('click', function() {
            let choices = []; 
            let images = [];
        
            const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
        
            checkboxes.forEach((checkbox) => {
                choices.push(checkbox.nextElementSibling.textContent.trim());
                images.push(checkbox.getAttribute('data-image'));
            });

            document.getElementById('userChoices').textContent = 'Vous avez choisi: ' + choices.join(',  ');
        
            const imagesContainer = document.getElementById('imagesContainer');
            imagesContainer.innerHTML = ''; // Efface les images précédentes
        
            images.forEach((image) => {
                const imgElement = document.createElement('img');
                imgElement.src = image;
                imgElement.style.maxWidth = '100px'; // Ajustez la taille de l'image selon vos besoins
                imagesContainer.appendChild(imgElement);
            });
        });
        
        document.getElementById('validateBtn').addEventListener('click', function() {
            let selectedValues = [];
            const selectedChoices = document.querySelectorAll('input[type="checkbox"]:checked');
            
            selectedChoices.forEach((choice) => {
                selectedValues.push(choice.value);
            });
            
            // Requête à l'API Spoonacular
            const apiKey = '6de7304103c9471ea3d59b2931dd2911'; // Remplacez 'YOUR_API_KEY' par votre clé d'API Spoonacular
            const number_of_recipes = 10;
            const ingredients = selectedValues.join(',');
            const url = `https://api.spoonacular.com/recipes/findByIngredients?ingredients=${ingredients}&number=${number_of_recipes}&apiKey=${apiKey}`;
            
            fetch(url)
            .then(response => response.json())
            .then(data => {
                const recipesContainer = document.getElementById('recipesContainer');
                recipesContainer.innerHTML = ''; // Efface les résultats précédents
                
                data.forEach((recipe) => {
                    // Créer un lien vers la recette
                    const recipeLink = document.createElement('a');
                    recipeLink.href = `https://spoonacular.com/recipes/${recipe.title}-${recipe.id}`;
                    recipeLink.target = "_blank"; // Ouvrir dans un nouvel onglet
                    recipeLink.title = recipe.title; // Ajouter le titre de la recette comme texte de survol

                    // Créer une image pour la recette
                    const recipeImage = document.createElement('img');
                    recipeImage.src = recipe.image; // URL de l'image de la recette
                    recipeImage.alt = recipe.title; // Texte alternatif pour l'image

                    // Ajouter l'image à l'élément du lien
                    recipeLink.appendChild(recipeImage);

                    // Ajouter le lien (avec l'image) à la liste des recettes
                    recipesContainer.appendChild(recipeLink);
                });
            })
            .catch(error => {
                console.error('Erreur lors de la recherche de recettes :', error);
            });
        });