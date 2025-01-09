import io

from flask import Flask, render_template, request
import pandas as pd
import sqlite3
import sys
app = Flask(__name__)
from PIL import Image
import base64

connexion = sqlite3.connect("inventaire.db", check_same_thread=False)
cursor = connexion.cursor()


def update_inventory(table_name, name, quantity):
    """Pour changer la valeur du nombre d'objet que l'on a"""
    cursor.execute(f"UPDATE {table_name} SET quantity=? WHERE name=?", (quantity,name))
    connexion.commit()


def get_quantity(table_name, name):
    """Pour connaitre le nombre d'objet que l'on a"""
    cursor.execute(f"SELECT quantity FROM {table_name} WHERE name=?",(name,))
    element = cursor.fetchone()
    if element is None:
        return None
    return element[0]


def get_all_items(table):
    cursor.execute(f"SELECT * FROM {table}")
    return cursor.fetchall()


def delete_from_inventory(table_name, name):
    cursor.execute(f"DELETE FROM {table_name} WHERE name=?", (name,))
    connexion.commit()

def order_received(name):
    """une livraison est arrivé; enleve toute la quantité en transit de l'objet recu et l ajoute a l'inventaire"""
    cursor.execute("SELECT * FROM commandes WHERE name=?",(name,))
    quantity = get_quantity("commandes", name)
    if cursor.fetchone() is None:
        print("eee")
        add_to_inventory("stock",name, quantity)
    else:
        new_quantity = get_quantity("stock", name) + quantity
        update_inventory("stock", name, new_quantity)
    delete_from_inventory("commandes",name)
    connexion.commit()

def add_to_inventory(table_name,name,quantity):
    """pour ajouter un nouvel objet"""
    cursor.execute(f"SELECT * FROM {table_name} WHERE name=?", (name,))
    if cursor.fetchone() is None:
        cursor.execute(f"INSERT INTO {table_name} VALUES(?,?,?)", (name + ".png",name,quantity))
    connexion.commit()

@app.route('/')
def start():
    return render_template('projet.html')
    

@app.route('/stock')
def afficher_stock():
    donnees = get_all_items("stock")
    return render_template('stock.html', donnees=donnees)

@app.route('/commandes')
def afficher_commandes():
    donnees = get_all_items("commandes")
    return render_template('commandes.html', donnees=donnees)

@app.post('/add_stock')
def add_stock():
    """pour ajouter un nombre d'objet a celui que l on a deja"""
    data = request.get_json()
    name = data.get("name")
    quantity = int(data.get("quantity"))
    new_quantity = get_quantity("stock", name) + quantity
    update_inventory("stock", name, new_quantity)
    return '', 204


@app.post('/remove_stock')
def remove_stock():
    """pour enlever un nombre d'objet a celui que l on a deja"""
    data = request.get_json()
    name = data.get("name")
    quantity = int(data.get("quantity"))
    new_quantity = get_quantity("stock", name) - quantity
    if new_quantity < 0:
        new_quantity = 0
    if new_quantity == 0:
        delete_from_inventory("stock", name)
    update_inventory("stock", name, new_quantity)
    return '', 204


@app.post('/create_stock')
def create_stock():
    data = request.get_json()
    name = data.get("name")
    if get_quantity("stock", name) != None:
        raise ValueError('le produit existe deja')
    else:
        imageb64 = data.get("image")
        imgdata = base64.b64decode(imageb64)
        filename = f'static/images/{name}.png'
        with open(filename, 'wb') as f:
            f.write(imgdata)
    number = int(data.get("quantity"))
    cursor.execute(f"INSERT INTO stock VALUES('{name}.png','{name}','{number}')")
    connexion.commit()
    return '', 204


@app.post('/arrived')
def arrived():
    data = request.get_json()
    name = data.get("name")
    order_received(name)
    return '', 204


@app.post('/order')
def order():
    data = request.get_json()
    name = data.get("name")
    if get_quantity("commandes", name) != None:
        raise ValueError('le produit existe deja')
    else:
        imageb64 = data.get("image")
        imgdata = base64.b64decode(imageb64)
        filename = f'static/images/{name}.png'
        with open(filename, 'wb') as f:
            f.write(imgdata)
    number = int(data.get("quantity"))
    cursor.execute(f"INSERT INTO commandes VALUES('{name}.png','{name}','{number}')")
    connexion.commit()
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)

