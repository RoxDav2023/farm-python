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

    form.style.display = "none"; // Pour cacher le formulaire
    next.style.display = "block"; // Pour afficher le paragraphe suivant
    nextButton.style.display = "none"; // Pour cacher le bouton "Next"
}

// meal generator //
const get_meal_btn = document.getElementById("get_meal");
const meal_container = document.getElementById("meal");

get_meal_btn.addEventListener("click", () => {
    fetch("https://www.themealdb.com/api/json/v1/1/random.php")
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

