document.getElementById('newsletter-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var email = document.getElementById('email').value;
    var messageDiv = document.getElementById('message');

    fetch('https://polar-plains-00718-3065c0aa9eda.herokuapp.com/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            email: email
        })
    })
    .then(response => response.json())
    .then(data => {
        messageDiv.textContent = data.message;
        messageDiv.style.color = 'green';
    })
    .catch(error => {
        messageDiv.textContent = 'Une erreur est survenue. Veuillez réessayer.';
        messageDiv.style.color = 'red';
    });
});
