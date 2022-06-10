from flask import Flask, redirect, render_template, request, g, url_for
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import flask_login
from flask_bcrypt import Bcrypt
import sqlite3

# INITIALISATION
app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['SECRET_KEY'] = 'clesecrete'

# CONNEXION/DECONNEXION
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

@app.route('/', methods = ["POST", "GET"])
def connexion():
    if request.method == "POST":
        db = get_db()
        cur = db.cursor()
        user = cur.execute("SELECT * FROM Compte WHERE identifiant=?", (request.form["identifiant"], )).fetchone()
        if user:
            new_user = User(user[0], user[1])
            try:
                new_user.password = user[1]
            except Exception:
                error = 'Invalid Username or Password'
                return render_template('connexion.html', error=error)

            if bcrypt.check_password_hash(new_user.password, request.form["password"]):
                login_user(new_user)
                if user[2] == 'Admin':
                    return redirect('accueilAdmin')
                return redirect('accueil')

            else:
                error = 'Invalid Username or Password'
                return render_template('connexion.html', error=error)
        else:
            error = 'Invalid Username or Password'
            return render_template('connexion.html', error=error)
    return render_template('connexion.html')

@app.route('/deconnexion', methods=['GET', 'POST'])
@login_required
def deconnexion():
    logout_user()
    return redirect("/")

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

# REPRESENTANT

@app.route('/inscription', methods = ["POST", "GET"])
def inscription():
    if request.method== "POST":
        db = get_db()
        cur = db.cursor()
        user = cur.execute("SELECT identifiant FROM Compte WHERE identifiant=?", (request.form["mail"], )).fetchone()
        if user:
            error = 'Cet utilisateur possède déjà un compte'
            return render_template("inscription.html", error = error)
        if request.form["password"] == request.form["password2"]:
            password = bcrypt.generate_password_hash(request.form["password"])
            cur.execute("INSERT INTO Compte(identifiant, mot_de_passe, type_compte) VALUES (?,?,?)",
                (request.form["id"], password, "Representant"))
            cur.execute("INSERT INTO Representant(nom_representant, prenom_representant, telephone, email, identifiant) VALUES (?,?,?,?,?)",
                (request.form["name"], request.form["prenom"], request.form["phone"], request.form["mail"], request.form["id"]))
            db.commit()
            return redirect("/")
        return render_template("inscription.html", error = "Les mots de passes sont différents")
    return render_template("inscription.html")

@app.route('/enfant/<int:code_enfant>', methods = ["POST", "GET"])
@login_required
def enfant(code_enfant):
    db = get_db()
    cur = db.cursor()
    if request.method == "POST":
        cur.execute("UPDATE Enfant SET nom_enfant=?, prenom_enfant=? WHERE code_enfant=?", (request.form["surname"], request.form["name"], code_enfant,))
        db.commit()
        return redirect(url_for('accueil'))

    representant = cur.execute("SELECT code_representant FROM Representant WHERE identifiant=?", (flask_login.current_user.name,)).fetchone()
    enfant = cur.execute("SELECT * from enfant WHERE code_representant=? and code_enfant=?", (representant[0], code_enfant,)).fetchone()
    enfants = cur.execute("SELECT code_enfant, prenom_enfant FROM Enfant AS E INNER JOIN Representant AS R ON E.code_representant = R.code_representant WHERE R.identifiant=?", (flask_login.current_user.name, )).fetchall()
    return render_template("enfant.html", enfants=enfants, enfant=enfant)

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
    enfants = cur.execute("SELECT code_enfant, prenom_enfant FROM Enfant AS E INNER JOIN Representant AS R ON E.code_representant = R.code_representant WHERE R.identifiant=?", (flask_login.current_user.name, )).fetchall()
    return render_template("actualites.html", enfants = enfants)

@app.route('/info')
@login_required
def info():
    db = get_db()
    cur = db.cursor()
    info = cur.execute("SELECT * FROM Representant WHERE identifiant=?",(flask_login.current_user.name, )).fetchone()
    compte = cur.execute("SELECT * from Compte WHERE identifiant=?", (flask_login.current_user.name, )).fetchone()
    return render_template("info.html", info = info, compte = compte)

@app.route('/info2', methods = ["GET", "POST"])
@login_required
def info2():
    db = get_db()
    cur = db.cursor()
    info = cur.execute("SELECT * FROM Representant WHERE identifiant=?",(flask_login.current_user.name, )).fetchone()
    if request.method== "POST": 
        user = cur.execute("SELECT * FROM Compte WHERE identifiant=?", (flask_login.current_user.name, )).fetchone()
        if user:
            new_user = User(user[0], user[1])

            if bcrypt.check_password_hash(new_user.password, request.form["password"]):
                error = "Vous ne pouvez pas réutiliser un ancien mot de passe"
                return render_template('info2.html', error = error, info = info)

            if request.form["password"] == request.form["password2"]:
                password = bcrypt.generate_password_hash(request.form["password"])
                cur.execute("UPDATE Compte SET mot_de_passe = ? WHERE identifiant = ?", (password, flask_login.current_user.name, ))
                db.commit()
                return redirect(url_for('info'))

            error = "Le mot de passe n'est pas le même"
            return render_template('info2.html', error = error, info = info)
            
    return render_template("info2.html", info = info)

   

@app.route('/accueil')
@login_required
def accueil():
    db = get_db()
    cur = db.cursor()
    enfants = cur.execute("SELECT code_enfant, prenom_enfant FROM Enfant AS E INNER JOIN Representant AS R ON E.code_representant = R.code_representant WHERE R.identifiant=?", (flask_login.current_user.name, )).fetchall()
    return render_template("accueil.html", enfants = enfants)

# ADMINISTRATEUR
@app.route('/accueilAdmin', methods=['GET', 'POST'])
@login_required
def accueilAdmin():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant=?", (flask_login.current_user.name,)).fetchone()
    if user[0] == 'Admin':
        return render_template('accueilAdmin.html')
    return redirect('accueil')

@app.route('/ajouterEnfant', methods=['GET', 'POST'])
@login_required
def ajouterEnfant():
    if request.method== "POST":
        db = get_db()
        cur = db.cursor()
        representant = cur.execute("SELECT code_representant FROM Representant WHERE identifiant=?", (flask_login.current_user.name,)).fetchone()
        cur.execute("INSERT INTO Enfant(nom_enfant, prenom_enfant, code_tarif, code_classe, code_representant) VALUES (?,?,1,1,?)", (request.form["surname"], request.form["name"], representant[0]))
        db.commit()
        return redirect('/accueil')
    return render_template('ajouterEnfant.html')


@app.route('/infosFamilles')
def infosFamille():
    db = get_db()
    cur = db.cursor()
    representants = cur.execute("SELECT * FROM representant").fetchall()
    return render_template('infosFamilles.html', representants=representants)

@app.route('/comptes', methods = ["POST", "GET"])
def comptes():
    if request.method == "POST":
        db = get_db()
        cur = db.cursor()
        user = cur.execute("SELECT identifiant FROM Compte WHERE identifiant=?", (request.form["id"], )).fetchone()
        if user:
            error = 'Cet utilisateur possède déjà un compte'
            return render_template("comptes.html", error = error)
        if (request.form["password"] == request.form["password2"]):
            password = bcrypt.generate_password_hash(request.form["password"])
            cur.execute("INSERT INTO Compte VALUES (?,?,?)", (request.form["id"], password, request.form["type"]))
            if request.form["type"] == "Representant":
                cur.execute("INSERT INTO Representant(nom_representant, prenom_representant, identifiant) VALUES (?,?,?)", (request.form["surname"], request.form["name"], request.form["id"],))
            else:
                cur.execute("INSERT INTO Enseignant(nom_enseignant, prenom_enseignant, identifiant) VALUES (?,?,?)", (request.form["surname"], request.form["name"], request.form["id"],))
            db.commit()
            return render_template("comptes.html", msg = 'Compte créé avec succès')
        return render_template("comptes.html", error = 'Les mots de passe ne correspondent pas')
    return render_template("comptes.html")

@app.route('/detailsFamille/<int:code_rep>', methods = ["POST", "GET"])
def editFamille(code_rep):
    db = get_db()
    cur = db.cursor()
    if request.method == "POST":
        password = bcrypt.generate_password_hash(request.form["password"])
        cur.execute("UPDATE Compte SET identifiant = ?, mot_de_passe = ? WHERE identifiant = ?", request.form["mail"], password, request.form["mail"])
        cur.execute("UPDATE Representant SET nom_representant=?, prenom_representant=?, telephone=?, email=? WHERE code_representant = ?", (request.form["surname"], request.form["name"], request.form["phone"], request.form["mail"], code_rep))
        db.commit()
        return redirect("/detailsFamille")
    
    representant = cur.execute("SELECT R.*, C.mot_de_passe FROM Representant AS R INNER JOIN Compte AS C ON R.email = C.identifiant WHERE R.code_representant = ?", (code_rep,)).fetchone()
    enfants = cur.execute("SELECT * FROM enfant WHERE code_representant = ?" ,  (code_rep,) ).fetchall()
    return render_template("detailsFamille.html", representant = representant, enfants = enfants)

@app.route('/detailsEnfants/<int:code_enf>', methods = ["POST", "GET"])
def editEnfant(code_enf):
    db = get_db()
    cur = db.cursor()
    # if request.method == "POST":
    #     cur.execute("UPDATE fpl SET cruiseSpeed=?, aircraftType=?, departureId=?, arrivalId=? "
    #         "WHERE id = ?",
    #         (request.form["cruiseSpeed"], request.form["aircraftType"], request.form["departureId"], request.form["arrivalId"], code_rep))
    #     db.commit()
    #     return redirect("/")
    
    enfant = cur.execute("SELECT * FROM enfant WHERE code_enfant = ?", (code_enf,)).fetchone()
    return render_template("detailsEnfants.html", enfant = enfant)


