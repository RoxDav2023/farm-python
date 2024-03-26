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
