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
        #cur.execute("UPDATE Enfant SET code_formule = ? WHERE code_enfant = ?", (request.form["formule"], code_enfant, ))
        #cur.execute("INSERT INTO Repas(date_repas, code_enfant) VALUES (?,?)", (request.form["repas"], code_enfant, ))
        cur.execute("DELETE FROM Mange WHERE code_enfant = ?", (code_enfant, ))
        i = 0
        if request.form.getlist('Lundi'):
            cur.execute("INSERT INTO Mange VALUES (?,?)", (request.form.getlist('Lundi')[0], code_enfant, ))
            i += 1
        if request.form.getlist('Mardi'):
            cur.execute("INSERT INTO Mange VALUES (?,?)", (request.form.getlist('Mardi')[0], code_enfant, ))
            i += 1
        if request.form.getlist('Jeudi'):
            cur.execute("INSERT INTO Mange VALUES (?,?)", (request.form.getlist('Jeudi')[0], code_enfant, ))
            i += 1
        if request.form.getlist('Vendredi'):
            cur.execute("INSERT INTO Mange VALUES (?,?)", (request.form.getlist('Vendredi')[0], code_enfant, ))
            i += 1
        if i == 0:
            i = 5
        cur.execute("UPDATE Enfant SET code_formule = ? WHERE code_enfant = ?", (i, code_enfant, ))

        db.commit()
        return redirect(url_for('accueil'))
    representant = cur.execute("SELECT code_representant FROM Representant WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    enfant = cur.execute("SELECT * FROM Enfant WHERE code_representant = ? and code_enfant = ?", (representant[0], code_enfant, )).fetchone()
    enfants = cur.execute("SELECT code_enfant, prenom_enfant FROM Enfant WHERE code_representant = ?", (representant[0], )).fetchall()
    formules = cur.execute("SELECT * FROM Formule").fetchall()
    joursManges = cur.execute("SELECT J.code_jour FROM Mange AS M INNER JOIN Jour AS J ON M.code_jour = J.code_jour WHERE M.code_enfant = ?", (code_enfant, )).fetchall()
    jours = cur.execute("SELECT * FROM  Jour").fetchall()
    now = datetime.datetime.today().strftime('%Y-%m-%d')
    return render_template('R_enfant.html', enfants = enfants, enfant = enfant, now = now, formules = formules, jours = jours, joursManges = joursManges)

@app.route('/facture', methods = ["GET"])
@login_required
def facture():

    mois=["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Aout","Septembre","Octobre","Novembre","Décembre"]
    return render_template('R_facture.html', mois = mois)

@app.route('/detailsFacture/<int:code_mois>', methods = ["GET"])
@login_required
def detailsFacture(code_mois):
    now = datetime.datetime.today().strftime('%Y-%m-%d')
    db = get_db()
    cur = db.cursor()
    if code_mois < 10:
        code_mois = '0' + str(code_mois)
    else:
        code_mois = str(code_mois)
    repas = cur.execute("SELECT R.date_repas, E.prenom_enfant, T.tarif FROM Repas AS R INNER JOIN Enfant AS E ON R.code_enfant = E.code_enfant "
     "INNER JOIN Representant AS Re ON Re.code_representant = E.code_representant INNER JOIN Tarif AS T ON E.code_tarif = T.code_tarif " 
     "WHERE Re.identifiant = ? AND strftime('%m', date_repas) = ? ORDER BY E.code_enfant, R.date_repas", (flask_login.current_user.name, code_mois, )).fetchall()
    representant = cur.execute("SELECT nom_representant, prenom_representant, code_representant FROM Representant WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    enfants = cur.execute("SELECT code_enfant, prenom_enfant FROM Enfant WHERE code_representant = ?", (representant[2], )).fetchall()
    return render_template('R_detailsFacture.html', now = now, repas = repas, representant = representant, enfants = enfants)

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
    enfants = cur.execute("SELECT code_enfant, prenom_enfant FROM Enfant AS E INNER JOIN Representant AS R ON E.code_representant = R.code_representant WHERE R.identifiant = ?", (flask_login.current_user.name, )).fetchall()
    return render_template('R_info.html', info = info, compte = compte, enfants= enfants)

@app.route('/info2', methods = ["GET", "POST"])
@login_required
def info2():
    db = get_db()
    cur = db.cursor()
    info = cur.execute("SELECT * FROM Representant WHERE identifiant = ?",(flask_login.current_user.name, )).fetchone()
    enfants = cur.execute("SELECT code_enfant, prenom_enfant FROM Enfant AS E INNER JOIN Representant AS R ON E.code_representant = R.code_representant WHERE R.identifiant = ?", (flask_login.current_user.name, )).fetchall()
    if request.method== "POST": 
        user = cur.execute("SELECT * FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
        if user:
            new_user = User(user[0], user[1])

            if bcrypt.check_password_hash(new_user.password, request.form["password"]):
                cur.execute("UPDATE Representant SET email=?,telephone=? WHERE identifiant = ?", (request.form["e-mail"],request.form["phone"], flask_login.current_user.name, ))
                db.commit()
                return redirect(url_for('info'))

            error = "Le mot de passe n'est pas le même"
            return render_template('R_modifInfo.html', error = error, info = info, enfants = enfants)
            
    return render_template('R_modifInfo.html', info = info, enfants = enfants)


@app.route('/info3', methods = ["GET", "POST"])
@login_required
def info3():
    db = get_db()
    cur = db.cursor()
    info = cur.execute("SELECT * FROM Representant WHERE identifiant = ?",(flask_login.current_user.name, )).fetchone()
    if request.method== "POST": 
        user = cur.execute("SELECT * FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
        enfants = cur.execute("SELECT code_enfant, prenom_enfant FROM Enfant AS E INNER JOIN Representant AS R ON E.code_representant = R.code_representant WHERE R.identifiant = ?", (flask_login.current_user.name, )).fetchall()
        if user: 
            new_user = User(user[0], user[1])
            if bcrypt.check_password_hash(new_user.password, request.form["fpassword"]):
                if bcrypt.check_password_hash(new_user.password, request.form["password"]):
                    error = 'Vous ne pouvez pas réutiliser un ancien mot de passe'
                    return render_template('R_modifInfosmdp.html', error = error, info = info, enfants = enfants)

                if request.form["password"] == request.form["password2"]:
                    password = bcrypt.generate_password_hash(request.form["password"])
                    cur.execute("UPDATE Compte SET mot_de_passe = ? WHERE identifiant = ?", (password, flask_login.current_user.name, ))
                    db.commit()
                    return redirect(url_for('info'))

                error = "Le mot de passe n'est pas le même"
                return render_template('R_modifInfosmdp.html', error = error, info = info, enfants = enfants)

            else :
                error = "Le mot de passe n'est pas le bon"
                return render_template("R_modifInfosmdp.html", error=error, info=info, enfants = enfants)
                
    return render_template('R_modifInfosmdp.html', info = info, enfants = enfants)
   

@app.route('/accueil', methods = ["GET"])
@login_required
def accueil():
    db = get_db()
    cur = db.cursor()
    enfants = cur.execute("SELECT code_enfant, prenom_enfant FROM Enfant AS E INNER JOIN Representant AS R ON E.code_representant = R.code_representant WHERE R.identifiant = ?", (flask_login.current_user.name, )).fetchall()
    return render_template('R_accueil.html', enfants = enfants)

@app.route('/ajoutRepas', methods = ["GET", "POST"])
@login_required
def ajoutRepas():
    db = get_db()
    cur = db.cursor()
    now = datetime.datetime.today()
    enfants = cur.execute("SELECT code_enfant, prenom_enfant FROM Enfant AS E INNER JOIN Representant AS R ON E.code_representant = R.code_representant WHERE R.identifiant = ?", (flask_login.current_user.name, )).fetchall()
    if request.method == "POST":
        date = datetime.datetime.strptime(request.form["repas"],'%Y-%m-%d')
        for enfant in enfants:
            if request.form.getlist(enfant[1]):
                check = cur.execute("SELECT * FROM Repas WHERE date_repas = ? AND code_enfant = ? ", (date, enfant[0])).fetchone()
                if not check and int(date.strftime('%d')) >= int(now.day) + 2:
                    cur.execute("INSERT INTO Repas(date_repas, code_enfant) VALUES (?,?)", (date.strftime('%Y-%m-%d'), enfant[0]))
            db.commit()
        return redirect(url_for('repas'))
    return render_template('R_ajoutRepas.html', enfants = enfants, now = now.strftime('%Y-%m-%d'))

@app.route('/repas', methods = ["GET"])
@login_required
def repas():
    db = get_db()
    cur = db.cursor()
    code_rep = cur.execute("SELECT code_representant FROM Representant WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    enfants = cur.execute("SELECT * FROM Enfant WHERE code_representant = ?", (code_rep[0], )).fetchall()
    repas = []
    now = datetime.datetime.today()
    date = now.strftime('%Y-%m-%d')
    for enfant in enfants:
        repas.append(cur.execute("SELECT * FROM Repas WHERE code_enfant = ? AND date_repas >= ? ORDER BY date_repas", (enfant[0], date , )).fetchall())
    limit = int(now.day) + 2
    date_limite = now.replace(day = limit)
    return render_template('R_repas.html', enfants = enfants, repasEnfants = repas, date_limite = date_limite.strftime('%Y-%m-%d'))

@app.route('/annuleRepas/<int:code_repas>', methods = ["GET"])
@login_required
def annuleRepas(code_repas):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM Repas WHERE code_repas = ?", (code_repas, ))
    db.commit()
    return redirect(url_for('repas'))

