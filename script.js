document.getElementById('newsletter-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const messageDiv = document.getElementById('message');

    fetch('save_email.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `email=${encodeURIComponent(email)}`
    })
    .then(response => response.text())
    .then(data => {
        messageDiv.textContent = data;
    })
    .catch(error => {
        messageDiv.textContent = 'Erreur lors de l\'inscription.';
    });
});
