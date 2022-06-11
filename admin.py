from main import *

# ADMINISTRATEUR
@app.route('/accueilAdmin', methods=['GET', 'POST'])
@login_required
def accueilAdmin():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        return render_template('A_accueilAdmin.html')
    return redirect('accueil')

@app.route('/ajouterEnfant/<int:code_rep>', methods=['GET', 'POST'])
@login_required
def ajouterEnfant(code_rep):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        representant = cur.execute("SELECT nom_representant, prenom_representant, code_representant FROM Representant WHERE code_representant = ?", (code_rep, )).fetchone()
        tarifs = cur.execute("SELECT * FROM Tarif").fetchall()
        classes = cur.execute("SELECT * FROM Classe").fetchall()
        if request.method == "POST":
            db = get_db()
            cur = db.cursor()
            cur.execute("INSERT INTO Enfant(nom_enfant, prenom_enfant, code_tarif, code_classe, code_representant, code_formule) VALUES (?,?,?,?,?,?)", 
                (request.form["surname"], request.form["name"], request.form["tarif"], request.form["classe"], code_rep, request.form["formule"], ))
            db.commit()
            return redirect(url_for('detailsFamille', code_rep = request.form["code"]))
        return render_template('A_ajouterEnfant.html', representant = representant, classes = classes, tarifs = tarifs)
    return redirect(url_for('acceuil'))

@app.route('/infosFamilles', methods = ["GET"])
@login_required
def infosFamille():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        representants = cur.execute("SELECT * FROM representant").fetchall()
        return render_template('A_infosFamilles.html', representants=representants)
    return redirect(url_for('acceuil'))

@app.route('/comptes', methods = ["POST", "GET"])
@login_required
def comptes():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        if request.method == "POST":
            user = cur.execute("SELECT identifiant FROM Compte WHERE identifiant = ?", (request.form["id"], )).fetchone()
            if user:
                error = 'Cet utilisateur possède déjà un compte'
                return render_template('A_comptes.html', error = error)
            if (request.form["password"] == request.form["password2"]):
                password = bcrypt.generate_password_hash(request.form["password"])
                cur.execute("INSERT INTO Compte VALUES (?,?,?)", (request.form["id"], password, request.form["type"], ))
                if request.form["type"] == 'Representant':
                    cur.execute("INSERT INTO Representant(nom_representant, prenom_representant, identifiant) VALUES (?,?,?)", (request.form["surname"], request.form["name"], request.form["id"], ))
                else:
                    cur.execute("INSERT INTO Enseignant(nom_enseignant, prenom_enseignant, identifiant) VALUES (?,?,?)", (request.form["surname"], request.form["name"], request.form["id"], ))
                db.commit()
                return render_template('A_comptes.html', msg = 'Compte créé avec succès')
            return render_template('A_comptes.html', error = 'Les mots de passe ne correspondent pas')
        return render_template('A_comptes.html')
    return redirect(url_for('acceuil'))

@app.route('/detailsFamille/<int:code_rep>', methods = ["POST", "GET"])
@login_required
def detailsFamille(code_rep):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        if request.method == "POST":
            password = bcrypt.generate_password_hash(request.form["password"])
            cur.execute("UPDATE Compte SET mot_de_passe = ? WHERE identifiant = ?", (password, request.form["id"], ))
            cur.execute("UPDATE Representant SET nom_representant=?, prenom_representant = ?, telephone = ?, email = ? WHERE code_representant = ?", 
            (request.form["surname"], request.form["name"], request.form["phone"], request.form["mail"], code_rep, ))
            db.commit()

        representant = cur.execute("SELECT R.*, C.mot_de_passe FROM Representant AS R INNER JOIN Compte AS C ON R.identifiant = C.identifiant WHERE R.code_representant = ?", (code_rep, )).fetchone()
        enfants = cur.execute("SELECT C.nom_classe, E.* FROM Enfant AS E INNER JOIN Classe AS C ON E.code_classe = C.code_classe WHERE code_representant = ?" ,  (code_rep, )).fetchall()
        return render_template('A_detailsFamille.html', representant = representant, enfants = enfants)
    return redirect(url_for('acceuil'))

@app.route('/detailsEnfant/<int:code_enf>', methods = ["POST", "GET"])
@login_required
def detailsEnfant(code_enf):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        if request.method == "POST":
            cur.execute("UPDATE Enfant SET nom_enfant = ?, prenom_enfant = ?, code_tarif = ?, code_classe = ? WHERE code_enfant = ?", 
            (request.form["surname"], request.form["name"], request.form["tarif"], request.form["classe"], code_enf, ))
            db.commit()
            code = cur.execute("SELECT code_representant FROM Enfant WHERE code_enfant = ?", (code_enf, )).fetchone()
            return redirect(url_for('detailsFamille', code_rep = code[0]))
        tarifs = cur.execute("SELECT * FROM Tarif").fetchall()
        classes = cur.execute("SELECT * FROM Classe").fetchall()
        formules = cur.execute("SELECT * FROM Formule").fetchall()
        enfant = cur.execute("SELECT * FROM Enfant WHERE code_enfant = ?", (code_enf,)).fetchone()
        return render_template('A_detailsEnfant.html', enfant = enfant, tarifs = tarifs, formules = formules, classes = classes)
    return redirect(url_for('acceuil'))


@app.route('/suppressionR/<int:code_rep>', methods = ["POST", "GET"])
@login_required
def suppressionR(code_rep):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        user = cur.execute("SELECT identifiant FROM Representant WHERE code_representant = ?", (code_rep, )).fetchone()
        cur.execute("DELETE FROM Compte WHERE identifiant = ?", (user[0], ))
        cur.execute("DELETE FROM Representant WHERE code_representant = ?", (code_rep, ))
        cur.execute("DELETE FROM Enfant WHERE code_representant = ?", (code_rep, ))
        db.commit()
        return redirect(url_for('infosFamilles'))
    return redirect(url_for('acceuil'))

@app.route('/suppressionE/<int:code_enf>', methods = ["POST", "GET"])
@login_required
def suppressionE(code_enf):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        code = cur.execute("SELECT code_representant FROM Enfant WHERE code_enfant = ?", (code_enf, )).fetchone()
        cur.execute("DELETE FROM Enfant WHERE code_enfant = ?", (code_enf, ))
        db.commit()
        return redirect(url_for('detailsFamille', code_rep = code[0]))
    return redirect(url_for('acceuil'))

@app.route('/infosEnseignants', methods = ["GET"])
@login_required
def infosEnseignants():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        enseignants = cur.execute("SELECT * FROM enseignant").fetchall()
        return render_template('A_infosEnseignants.html', enseignants=enseignants)

@app.route('/detailsEnseignant/<int:code_ens>', methods = ["POST", "GET"])
@login_required
def detailsEnseignant(code_ens):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        if request.method == "POST":
            password = bcrypt.generate_password_hash(request.form["password"])
            cur.execute("UPDATE Compte SET mot_de_passe = ? WHERE identifiant = ?", (password, request.form["id"], ))
            cur.execute("UPDATE Enseignant SET nom_enseignant=?, prenom_enseignant = ? WHERE code_enseignant = ?", 
            (request.form["surname"], request.form["name"], code_ens, ))
            db.commit()

        enseignant = cur.execute("SELECT Ens.*, C.mot_de_passe FROM Enseignant AS Ens INNER JOIN Compte AS C ON Ens.identifiant = C.identifiant WHERE Ens.code_enseignant = ?", (code_ens, )).fetchone()
        classes = cur.execute("SELECT C.* FROM Classe AS C INNER JOIN Enseigne AS E ON C.code_classe = E.code_classe WHERE E.code_enseignant = ?" ,  (code_ens, )).fetchall()
        return render_template('A_detailsEnseignant.html', enseignant = enseignant, classes = classes)
    return redirect(url_for('acceuil'))




























@app.route('/infosTarifs', methods = ["GET"])
@login_required
def infosTarifs():
    #Cesar/Alice
    return render_template('A_infosTarifs.html')

@app.route('/infosClasses', methods = ["GET"])
@login_required
def infosClasses():
    #Cesar/Alice
    return render_template('A_infosClasses.html')


