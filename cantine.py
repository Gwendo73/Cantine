from flask import Flask, redirect, render_template, request,g
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import flask_login
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['SECRET_KEY'] = 'clesecrete'

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    cur = db.cursor()
    user = cur.execute('SELECT identifiant, mot_de_passe FROM Compte WHERE identifiant=?', (user_id, )).fetchone()
    user = User(user[0], user[1])
    return user

class User(UserMixin):

    def __init__(self, username, password):
        self.name = username
        self.password = password

    @property
    def id(self):
        return self.name

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
    if request.method == "POST":
        db = get_db()
        cur = db.cursor()
        user = cur.execute("SELECT identifiant, mot_de_passe FROM Compte WHERE identifiant=?", (request.form["mail"],)).fetchone()
        new_user = User(user[0], user[1])
        if new_user:
            if bcrypt.check_password_hash(new_user.password, request.form["password"]):
                login_user(new_user)
                return redirect("accueil")
    return render_template("connexion.html")


@app.route('/inscription', methods = ["POST", "GET"])
def inscription():
    if request.method== "POST":
        db = get_db()
        cur = db.cursor()
        user = cur.execute("SELECT identifiant FROM Compte WHERE identifiant=?", (request.form["mail"], )).fetchone()
        if user:
            return render_template("inscription.html", invalid = True)
        password = bcrypt.generate_password_hash(request.form["password"])
        cur.execute("INSERT INTO Compte(identifiant, mot_de_passe, type_compte) VALUES (?,?,?)",
            (request.form["mail"], password, "Representant"))
        cur.execute("INSERT INTO Representant(nom_representant, prenom_representant, telephone, email) VALUES (?,?,?,?)",
            (request.form["name"], request.form["prenom"], request.form["phone"], request.form["mail"]))
        db.commit()
        return redirect("/")
    return render_template("inscription.html")

@app.route('/enfant')
@login_required
def enfant():
    db = get_db()
    cur = db.cursor()
    enfants = cur.execute("SELECT prenom_enfant from enfant WHERE code_representant=1").fetchall()
    return render_template("enfant.html", enfants=enfants)

@app.route('/facture')
@login_required
def facture():
    mois=["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Aout","Septembre","Octobre","Novembre","Décembre"]
    return render_template("facture.html", mois=mois)

@app.route('/actu')
@login_required
def actu():
    db = get_db()
    cur = db.cursor()
    enfants = cur.execute("SELECT prenom_enfant from enfant WHERE code_representant=1").fetchall()
    return render_template("actualites.html", enfants = enfants)

@app.route('/info')
@login_required
def info():
    return render_template("info.html")

@app.route('/deconnexion', methods=['GET', 'POST'])
@login_required
def deconnexion():
    logout_user()
    return redirect("/")

@app.route('/accueil')
@login_required
def accueil():
    db = get_db()
    cur = db.cursor()
    enfants = cur.execute("SELECT prenom_enfant FROM Enfant AS E INNER JOIN Representant AS R ON E.code_representant = R.code_representant WHERE R.email=?", (flask_login.current_user.name, )).fetchall()
    return render_template("accueil.html", enfants = enfants)

