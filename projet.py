from flask import Flask, render_template, request
import pandas as pd
import sqlite3
import sys
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 10000

connexion = sqlite3.connect("inventaire.db", check_same_thread=False)
cursor = connexion.cursor()


def update_inventory(table_name, name, quantity):
    """Pour changer la valeur du nombre d'objet que l'on a"""
    cursor.execute(f"UPDATE {table_name} SET quantity=? WHERE name=?", (quantity,name))
    connexion.commit()


def get_quantity(table_name,name):
    """Pour connaitre le nombre d'objet que l'on a"""
    cursor.execute(f"SELECT quantity FROM {table_name} WHERE name=?",(name,))
    return cursor.fetchone()[0]


def get_all_items():
    cursor.execute("SELECT * FROM stock")
    return cursor.fetchall()


def delete_from_inventory(table_name, name):
    cursor.execute(f"DELETE FROM {table_name} WHERE name=?", (name,))
    connexion.commit()


@app.route('/')
def start():
    return render_template('projet.html')
    

@app.route('/table')
def afficher_tableau():
    donnees = get_all_items()
    return render_template('table.html', donnees=donnees)


@app.post('/add')
def add_stock():
    """pour ajouter un nombre d'objet a celui que l on a deja"""
    print(request)
    name = str(request.json)
    new_quantity = get_quantity("stock", name) + 1
    update_inventory("stock", name, new_quantity)
    return '', 204


@app.post('/remove')
def remove_stock():
    """pour enlever un nombre d'objet a celui que l on a deja"""
    name = str(request.json)
    new_quantity = get_quantity("stock", name) - 1
    if new_quantity < 0:
        new_quantity = 0
        raise ValueError("Not enough stock to remove")
    if new_quantity == 0:
        delete_from_inventory("stock", name)
    update_inventory("stock", name, new_quantity)
    return '', 204
    

if __name__ == '__main__':
    app.run(debug=True)

