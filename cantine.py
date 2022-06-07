from ast import If
from pydoc import render_doc
from flask import Flask, redirect, render_template, request,g
import sqlite3

app = Flask(__name__)
#IMPORT DE LA BASE DE DONNÉE

DATABASE = "db/cantine.db"

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

#FENETRE

@app.route('/', methods = ["POST", "GET"])
def connexion():
    if request.method== "POST":
        return render_template("accueil.html")
    return render_template("pageconnexion.html")


@app.route('/pageinscription', methods = ["POST", "GET"])
def inscription():
    if request.method== "POST":
        return render_template("accueil.html")
    return render_template("pageinscription.html")

@app.route('/enfant')
def enfant():
    db = get_db()
    cur = db.cursor()
    enfants = cur.execute("SELECT prenom_enfant from enfant WHERE code_representant=1").fetchall()
    return render_template("enfant.html", enfants=enfants)

@app.route('/facture')
def facture():
    mois=["janvier","février","mars","avril","mai","juin","juillet","aout","septembre","octobre","novembre","décembre"];
    return render_template("facture.html", mois=mois)

@app.route('/actu')
def actu():
    return render_template("actualites.html")

@app.route('/deconnexion')
def deconnexion():
    return render_template("deconnexion.html")


