document.getElementById('newsletter-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevents the default form submission

    const email = document.getElementById('email').value;
    const messageDiv = document.getElementById('message');

    fetch('/submit', {
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
