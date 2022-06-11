from main import *
# REPRESENTANT

@app.route('/inscription', methods = ["POST", "GET"])
def inscription():
    if request.method== "POST":
        db = get_db()
        cur = db.cursor()
        user = cur.execute("SELECT identifiant FROM Compte WHERE identifiant = ?", (request.form["mail"], )).fetchone()
        if user:
            error = 'Cet utilisateur possède déjà un compte'
            return render_template("R_inscription.html", error = error)
        if request.form["password"] == request.form["password2"]:
            password = bcrypt.generate_password_hash(request.form["password"])
            cur.execute("INSERT INTO Compte(identifiant, mot_de_passe, type_compte) VALUES (?,?,?)",
                (request.form["id"], password, "Representant", ))
            cur.execute("INSERT INTO Representant(nom_representant, prenom_representant, telephone, email, identifiant) VALUES (?,?,?,?,?)",
                (request.form["name"], request.form["prenom"], request.form["phone"], request.form["mail"], request.form["id"], ))
            db.commit()
            return redirect('/')
        error = 'Les mots de passes sont différents'
        return render_template('R_inscription.html', error = error)
    return render_template('R_inscription.html')

@app.route('/enfant/<int:code_enfant>', methods = ["POST", "GET"])
@login_required
def enfant(code_enfant):
    db = get_db()
    cur = db.cursor()
    if request.method == "POST":
        cur.execute("INSERT INTO Repas(date_repas, code_enfant) VALUES (?,?)", (request.form["repas"], code_enfant, ))
        db.commit()
        return redirect(url_for('accueil'))

    representant = cur.execute("SELECT code_representant FROM Representant WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    enfant = cur.execute("SELECT * from enfant WHERE code_representant = ? and code_enfant = ?", (representant[0], code_enfant, )).fetchone()
    enfants = cur.execute("SELECT code_enfant, prenom_enfant FROM Enfant WHERE code_representant = ?", (representant[0], )).fetchall()
    now = datetime.datetime.today().strftime('%Y-%m-%d')
    return render_template('R_enfant.html', enfants = enfants, enfant = enfant, now = now)

@app.route('/facture', methods = ["GET"])
@login_required
def facture():
    mois=["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Aout","Septembre","Octobre","Novembre","Décembre"]
    return render_template('R_facture.html', mois = mois)

@app.route('/actu', methods = ["GET"])
@login_required
def actu():
    db = get_db()
    cur = db.cursor()
    enfants = cur.execute("SELECT code_enfant, prenom_enfant FROM Enfant AS E INNER JOIN Representant AS R ON E.code_representant = R.code_representant WHERE R.identifiant=?", (flask_login.current_user.name, )).fetchall()
    return render_template('R_actualites.html', enfants = enfants)

@app.route('/info', methods = ["GET"])
@login_required
def info():
    db = get_db()
    cur = db.cursor()
    info = cur.execute("SELECT * FROM Representant WHERE identifiant = ?",(flask_login.current_user.name, )).fetchone()
    compte = cur.execute("SELECT * from Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    return render_template('R_info.html', info = info, compte = compte)

@app.route('/info2', methods = ["GET", "POST"])
@login_required
def info2():
    db = get_db()
    cur = db.cursor()
    info = cur.execute("SELECT * FROM Representant WHERE identifiant = ?",(flask_login.current_user.name, )).fetchone()
    if request.method== "POST": 
        user = cur.execute("SELECT * FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
        if user:
            new_user = User(user[0], user[1])

            if bcrypt.check_password_hash(new_user.password, request.form["password"]):
                error = 'Vous ne pouvez pas réutiliser un ancien mot de passe'
                return render_template('R_modifInfo.html', error = error, info = info)

            if request.form["password"] == request.form["password2"]:
                password = bcrypt.generate_password_hash(request.form["password"])
                cur.execute("UPDATE Compte SET mot_de_passe = ? WHERE identifiant = ?", (password, flask_login.current_user.name, ))
                db.commit()
                return redirect(url_for('info'))

            error = "Le mot de passe n'est pas le même"
            return render_template('R_modifInfo.html', error = error, info = info)
            
    return render_template('R_modifInfo.html', info = info)

   

@app.route('/accueil', methods = ["GET"])
@login_required
def accueil():
    db = get_db()
    cur = db.cursor()
    enfants = cur.execute("SELECT code_enfant, prenom_enfant FROM Enfant AS E INNER JOIN Representant AS R ON E.code_representant = R.code_representant WHERE R.identifiant = ?", (flask_login.current_user.name, )).fetchall()
    return render_template('R_accueil.html', enfants = enfants)

@app.route('/repas', methods = ["GET"])
@login_required
def repas():
    db = get_db()
    cur = db.cursor()
    code_rep = cur.execute("SELECT code_representant FROM Representant WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    enfants = cur.execute("SELECT * FROM Enfant WHERE code_representant = ?", (code_rep[0], )).fetchall()
    repas = []
    now = datetime.datetime.today().strftime('%Y-%m-%d')
    for enfant in enfants:
        repas.append(cur.execute("SELECT * FROM Repas WHERE code_enfant = ? AND date_repas > ?", (enfant[0], now, )).fetchall())

    return render_template('R_repas.html', enfants = enfants, repas = repas)
