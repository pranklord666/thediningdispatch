import requests

# Configuration
app_url = 'https://polar-plains-00718.herokuapp.com'  # URL de votre application Heroku
local_path = 'C:\\Pranklord666\\thediningdispatch\\emails.csv'

# Télécharger le fichier depuis la route /download-emails
response = requests.get(f'{app_url}/download-emails')

if response.status_code == 200:
    with open(local_path, 'wb') as file:
        file.write(response.content)
    print(f"Fichier téléchargé et enregistré à {local_path}")
else:
    print(f"Erreur lors du téléchargement : {response.status_code} - {response.text}")
