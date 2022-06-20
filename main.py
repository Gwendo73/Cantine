from flask import Flask, redirect, render_template, request, g, url_for
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import flask_login
from flask_bcrypt import Bcrypt
import sqlite3
import datetime
import pandas as pd
import locale


locale.setlocale(locale.LC_ALL, 'fr_FR')

# INITIALISATION
app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['SECRET_KEY'] = 'clesecrete'

# CONNEXION/DECONNEXION

class User(UserMixin):

    def __init__(self, username, password):
        self.name = username
        self.password = password

    @property
    def id(self):
        return self.name

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    cur = db.cursor()
    user = cur.execute('SELECT identifiant, mot_de_passe FROM Compte WHERE identifiant=?', (user_id, )).fetchone()
    return User(user[0], user[1])

# BASE DE DONNEES

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
        
@app.route('/', methods = ["POST", "GET"])
def connexion():
    # Permet de chiffrer les mots de passe à la première création de la base de données.
    # db = get_db()
    # cur = db.cursor()
    # users = cur.execute("SELECT * FROM Compte").fetchall()
    # for user in users:
    #     password = bcrypt.generate_password_hash(user[1])
    #     cur.execute("UPDATE Compte SET mot_de_passe = ? WHERE identifiant = ?", (password, user[0],) )
    #     db.commit()

    if request.method == "POST":
        db = get_db()
        cur = db.cursor()
        user = cur.execute("SELECT * FROM Compte WHERE identifiant=?", (request.form["identifiant"], )).fetchone()
        if user:
            new_user = User(user[0], user[1])
            if bcrypt.check_password_hash(new_user.password, request.form["password"]):
                login_user(new_user)
                if user[2] == 'Admin':
                    return redirect(url_for('accueilAdmin'))
                if user[2] == 'Enseignant':
                    return redirect(url_for('accueilEnseignant'))
                if user[2] == 'Representant':
                    return redirect(url_for('actu'))
                
            else:
                error = 'Invalid Username or Password'
                return render_template('G_connexion.html', error=error)
        else:
            error = 'Invalid Username or Password'
            return render_template('G_connexion.html', error=error)
    return render_template('G_connexion.html')

@app.route('/deconnexion', methods=['GET', 'POST'])
@login_required
def deconnexion():
    logout_user()
    return render_template('G_deconnexion.html')

### Fonction permettant de changer la date par défaut afin d'effectuer des simulations
def choixDate():
    # Pour tester depuis le début de l'année
    #return datetime.datetime(2021, 9, 1)
    # Pour tester à la date actuelle
    return datetime.datetime.today()

import representant
import admin
import enseignant
