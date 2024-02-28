// Get all elements with the class "assign-link"
var assignLinks = document.querySelectorAll('.assign-link');

// Loop through each link and attach a click event listener
assignLinks.forEach(function(link) {
    link.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default behavior of the link

        // Prompt the user for input
        var builderId = prompt('Enter Builder ID:');
        
        // If the user entered an ID, append it to the link's href attribute
        if (builderId) {
            this.href += '&builder_id=' + builderId;
        }
    });
});