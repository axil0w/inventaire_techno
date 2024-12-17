from flask import Flask, render_template
import pandas as pd
import sqlite3
app = Flask(__name__)


connexion = sqlite3.connect("inventaire.db", check_same_thread=False)
cursor = connexion.cursor()


def get_all_items():
    cursor.execute("SELECT * FROM stock")
    return cursor.fetchall()

@app.route('/')
def afficher_tableau():
    donnees = get_all_items()	
    return render_template('table.html', donnees=donnees)

if __name__ == '__main__':
    app.run(debug=True)
