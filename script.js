document.getElementById('newsletter-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const messageDiv = document.getElementById('message');

    fetch('https://formspree.io/f/xyzyndrd', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.ok) {
            messageDiv.textContent = 'Merci de votre inscription!';
        } else {
            messageDiv.textContent = 'Erreur lors de l\'inscription.';
        }
    })
    .catch(error => {
        messageDiv.textContent = 'Erreur lors de l\'inscription.';
    });
});
