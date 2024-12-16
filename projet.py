from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Exemple de données pour le tableau
donnees = [
    {'nom': 'Jean Dupont', 'age': 35, 'ville': 'Paris'},
    {'nom': 'Marie Martin', 'age': 28, 'ville': 'Lyon'},
    {'nom': 'Pierre Durand', 'age': 42, 'ville': 'Marseille'},
    {'nom': 'Sophie Leroy', 'age': 31, 'ville': 'Toulouse'}
]

@app.route('/')
def afficher_tableau():
    return render_template('table.html', donnees=donnees)

if __name__ == '__main__':
    app.run(debug=True)

