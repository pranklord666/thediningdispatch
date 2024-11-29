@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    csv_file_path = '/tmp/emails.csv'  # Emplacement temporaire pour Heroku
    
    # Créer le fichier s'il n'existe pas
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, 'w') as file:
            file.write('email\n')
    
    # Ajouter l'email au fichier
    with open(csv_file_path, 'a') as file:
        writer = csv.writer(file)
        writer.writerow([email])
    
    return jsonify({'message': 'Email received'})
