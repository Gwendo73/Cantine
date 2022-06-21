from main import *

### ACCEUIL ADMIN

@app.route('/accueilAdmin', methods=['GET', 'POST'])
@login_required
def accueilAdmin():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        if request.method=="POST" :
            if request.form["password"] == request.form["password2"]:
                password = bcrypt.generate_password_hash(request.form["password"])
                cur.execute("UPDATE Compte SET mot_de_passe = ? WHERE identifiant = ?", (password, flask_login.current_user.name, ))
                db.commit()
                return redirect('/')
            error = 'Les mots de passes sont différents'
            return render_template('A_accueilAdmin.html', error = error)
        return render_template('A_accueilAdmin.html')
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))

### AJOUT ENFANT

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
        formules = cur.execute("SELECT * FROM Formule").fetchall()
        if request.method == "POST":
            db = get_db()
            cur = db.cursor()
            cur.execute("INSERT INTO Enfant(nom_enfant, prenom_enfant, code_tarif, code_classe, code_representant, code_formule) VALUES (?,?,?,?,?,?)", 
                (request.form["surname"], request.form["name"], request.form["tarif"], request.form["classe"], code_rep, 5, ))
            db.commit()
            return redirect(url_for('detailsFamille', code_rep = request.form["code"]))
        return render_template('A_ajouterEnfant.html', representant = representant, classes = classes, tarifs = tarifs, formules = formules)
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil')) 

### AJOUT VACANCES

@app.route('/ajoutVacances', methods=['GET', 'POST'])
@login_required
def ajoutVacances():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        if request.method == "POST":
            db = get_db()
            cur = db.cursor()
            continueW = True
            insert = True
            new_date = datetime.datetime.strptime(request.form["date_debut"], '%Y-%m-%d')
            conges = cur.execute("SELECT * FROM Conge").fetchall()
            while continueW:
                if new_date.strftime('%Y-%m-%d') == request.form["date_fin"]:
                    continueW = False
                for conge in conges:
                    if new_date.strftime('%Y-%m-%d')  == conge[0]:
                        insert = False
                        break
                if insert:
                    cur.execute("INSERT INTO Conge(date_conge) VALUES (?)", (new_date.strftime('%Y-%m-%d'), )) 

                    cur.execute("DELETE FROM Repas WHERE date_repas = ?", (new_date.strftime('%Y-%m-%d'), ))
                insert = True
                new_date += datetime.timedelta(days = 1)
            db.commit()
            return redirect(url_for('calendrier'))
        return render_template('A_ajoutVacances.html')
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant')) 
    return redirect(url_for('accueil'))

### ANNULE VACANCES

@app.route('/annuleVacances/<conges>', methods = ["GET"])
@login_required
def annuleVacances(conges):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        cur.execute("DELETE FROM Conge WHERE date_conge = ?", (conges, ))
        db.commit()
        return redirect(url_for('calendrier'))
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant')) 
    return redirect(url_for('accueil'))

### CALENDRIER

@app.route('/calendrier', methods=['GET', 'POST'])
@login_required
def calendrier():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        ### Permet de set les mercredi, samedi, dimanche de l'année en tant que congés
        # now = choixDate()
        # anneeBis = now.year
        # if now.month > 7:
        #     anneeBis += 1
        # debut = datetime.datetime(now.year, now.month, now.day).strftime('%m/%d/%Y')
        # fin = datetime.datetime(anneeBis, 7, 15).strftime('%m/%d/%Y')
        # dates = pd.date_range(start=debut, end=fin, freq='W-WED').strftime('%Y-%m-%d').tolist()
        # for date in dates:
        #     cur.execute("INSERT INTO Conge(date_conge) VALUES (?)", (date, )) 
        #     cur.execute("DELETE FROM Repas WHERE date_repas = ?", (date, ))
        # dates = pd.date_range(start=debut, end=fin, freq='W-SAT').strftime('%Y-%m-%d').tolist()
        # for date in dates:
        #     cur.execute("INSERT INTO Conge(date_conge) VALUES (?)", (date, )) 
        #     cur.execute("DELETE FROM Repas WHERE date_repas = ?", (date, ))
        # dates = pd.date_range(start=debut, end=fin, freq='W-SUN').strftime('%Y-%m-%d').tolist()
        # for date in dates:
        #     cur.execute("INSERT INTO Conge(date_conge) VALUES (?)", (date, ))
        #     cur.execute("DELETE FROM Repas WHERE date_repas = ?", (date, ))
        page_size = 10
        page = int(request.args.get('page', '1'))
        now = choixDate().strftime('%Y-%m-%d')
        conges = cur.execute("SELECT * FROM Conge WHERE date_conge >= ? ORDER BY date_conge", (now, )).fetchall()
        date = []
        db.commit()
        for conge in conges:
            date.append(datetime.datetime.strptime(conge[0], '%Y-%m-%d').strftime('%A %d/%m/%Y'))
        page_total = int(len(conges)/page_size) + 1
        return render_template('A_calendrier.html', conges = conges[((page-1) * page_size) : (page * page_size)], date = date, list_of_page = range(1, page_total + 1), page_total = page_total, page = page)
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))

### COMPTES

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
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))

### CREATION CLASSE

@app.route('/creerClasse', methods=['GET', 'POST'])
@login_required
def creerClasse():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        types_classe = cur.execute("SELECT * FROM typedeclasse").fetchall()
        classes = cur.execute("SELECT * FROM Classe").fetchall()
        if request.method == "POST":
            db = get_db()
            cur = db.cursor()
            cur.execute("INSERT INTO classe(nom_classe, code_type) VALUES (?,?)", 
                (request.form["classe"], request.form["type_classe"], ))
            db.commit()
            return redirect(url_for('infosClasses'))
        return render_template('A_creerClasse.html', types_classe = types_classe, classes = classes)
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))

### CREATION TARIF 

@app.route('/creerTarif', methods=['GET', 'POST'])
@login_required
def creerTarif():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        # types_classe = cur.execute("SELECT * FROM typedeclasse").fetchall()
        # classes = cur.execute("SELECT * FROM Classe").fetchall()
        if request.method == "POST":
            db = get_db()
            cur = db.cursor()
            cur.execute("INSERT INTO tarif(nom_tarif, tarif) VALUES (?,?)", 
                (request.form["tarif"], request.form["prix"], ))
            db.commit()
            return redirect(url_for('infosTarifs'))
        return render_template('A_creerTarif.html')
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))

### DETAILS CLASSE

@app.route('/detailsClasse/<int:code_classe>', methods = ["GET", "POST"])
@login_required
def detailsClasse(code_classe):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        enseignants = cur.execute("SELECT E.nom_enseignant, E.prenom_enseignant, E.code_enseignant FROM Enseignant AS E INNER JOIN Enseigne AS Ens ON E.code_enseignant = Ens.code_enseignant WHERE code_classe = ?", (code_classe, )).fetchall()
        classe = cur.execute("SELECT nom_classe, code_classe, code_type FROM Classe WHERE code_classe = ?", (code_classe, )).fetchone()
        types = cur.execute ("SELECT * FROM TypeDeClasse").fetchall()
        enfants = cur.execute("SELECT nom_enfant, prenom_enfant, code_enfant FROM Enfant WHERE code_classe = ?", (code_classe, )).fetchall()
        if request.method == "POST":
            cur.execute("UPDATE Classe SET nom_classe = ?, code_type = ? WHERE code_classe = ?", (request.form["name"], request.form["classe"], code_classe, ))
            db.commit()
            return redirect(url_for('infosClasses'))
        return render_template('A_detailsClasse.html', enseignants = enseignants, enfants = enfants, classe = classe, types = types)
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))

### DETAILS ENFANT 

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
        classes = cur.execute("SELECT C.code_classe, C.nom_classe, T.niveau_classe, T.type_classe FROM Classe AS C INNER JOIN TypeDeClasse AS T ON C.code_type = T.code_type ORDER BY C.code_type, C.nom_classe").fetchall()
        formules = cur.execute("SELECT * FROM Formule").fetchall()
        enfant = cur.execute("SELECT code_enfant, nom_enfant, prenom_enfant, code_tarif, code_classe, code_representant FROM Enfant WHERE code_enfant = ?", (code_enf,)).fetchone()
        return render_template('A_detailsEnfant.html', enfant = enfant, tarifs = tarifs, formules = formules, classes = classes)
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))

### DETAILS ENSEIGNANT

@app.route('/detailsEnseignant/<int:code_ens>', methods = ["POST", "GET"])
@login_required
def detailsEnseignant(code_ens):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        if request.method == "POST":
            password = bcrypt.generate_password_hash(request.form["password"])
            cur.execute("UPDATE Compte SET mot_de_passe = ? WHERE identifiant = ?", (password, request.form["identifiant"], ))
            cur.execute("UPDATE Enseignant SET nom_enseignant=?, prenom_enseignant = ? WHERE code_enseignant = ?", 
            (request.form["surname"], request.form["name"], code_ens, ))
            db.commit()

        enseignant = cur.execute("SELECT Ens.*, C.mot_de_passe FROM Enseignant AS Ens INNER JOIN Compte AS C ON Ens.identifiant = C.identifiant WHERE Ens.code_enseignant = ?", (code_ens, )).fetchone()
        classes = cur.execute("SELECT C.* FROM Classe AS C INNER JOIN Enseigne AS E ON C.code_classe = E.code_classe WHERE E.code_enseignant = ? ORDER BY code_type, nom_classe" ,  (code_ens, )).fetchall()
        return render_template('A_detailsEnseignant.html', enseignant = enseignant, classes = classes)
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))

### DETAILS FAMILLE

@app.route('/detailsFamille/<int:code_rep>', methods = ["POST", "GET"])
@login_required
def detailsFamille(code_rep):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        if request.method == "POST":
            cur.execute("UPDATE Representant SET nom_representant=?, prenom_representant = ?, telephone = ?, email = ? WHERE code_representant = ?", 
            (request.form["surname"], request.form["name"], request.form["phone"], request.form["mail"], code_rep, ))
            db.commit()

        representant = cur.execute("SELECT R.*, C.mot_de_passe FROM Representant AS R INNER JOIN Compte AS C ON R.identifiant = C.identifiant WHERE R.code_representant = ?", (code_rep, )).fetchone()
        enfants = cur.execute("SELECT E.nom_enfant, E.prenom_enfant, C.nom_classe, E.code_enfant FROM Enfant AS E INNER JOIN Classe AS C ON E.code_classe = C.code_classe WHERE code_representant = ? ORDER BY E.nom_enfant, E.prenom_enfant" ,  (code_rep, )).fetchall()
        return render_template('A_detailsFamille.html', representant = representant, enfants = enfants)
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))

### DETAILS TARIF

@app.route('/detailsTarif/<int:code_tarif>', methods = ["GET", "POST"])
@login_required
def detailsTarif(code_tarif):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        tarif = cur.execute("SELECT * FROM Tarif WHERE code_tarif = ?", (code_tarif, )).fetchone()
        enfants = cur.execute("SELECT code_enfant, nom_enfant, prenom_enfant FROM Enfant WHERE code_tarif = ?", (code_tarif, )).fetchall()
        if request.method == "POST":
            cur.execute("UPDATE Tarif SET nom_tarif = ?, tarif = ? WHERE code_tarif = ?", (request.form["nom_tarif"], request.form["tarif"], code_tarif, ))
            db.commit()
            return redirect(url_for('infosTarifs'))
        return render_template('A_detailsTarif.html', enfants = enfants, tarif = tarif)
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))

### INFOS CLASSES

@app.route('/infosClasses', methods = ["GET"])
@login_required
def infosClasses():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        classes = cur.execute("SELECT C.code_classe, C.nom_classe, T.niveau_classe, T.type_classe FROM Classe AS C INNER JOIN TypeDeClasse AS T ON C.code_type = T.code_type ORDER BY C.code_type, C.nom_classe").fetchall()
        return render_template('A_infosClasses.html', classes=classes)
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))

### INFOS ENFANTS

@app.route('/infosEnfants', methods = ["GET"])
@login_required
def infosEnfants():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        page_size = 10
        page = int(request.args.get('page', '1'))
        enfants = cur.execute("SELECT E.nom_enfant, E.prenom_enfant, C.nom_classe, T.nom_tarif, R.nom_representant, R.prenom_representant, E.code_enfant FROM Enfant AS E "
        "INNER JOIN Classe AS C ON E.code_classe = C.code_classe INNER JOIN Tarif AS T ON T.code_tarif = E.code_tarif "
        "INNER JOIN Representant AS R ON R.code_representant = E.code_representant ORDER BY E.nom_enfant, E.prenom_enfant").fetchall()
        page_total = int(len(enfants)/page_size) + 1
        return render_template('A_infosEnfants.html', enfants=enfants[((page-1) * page_size) : (page * page_size)], list_of_page = range(1, page_total + 1), page_total = page_total, page = page)
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))

###  INFOS ENSEIGNANTS

@app.route('/infosEnseignants', methods = ["GET"])
@login_required
def infosEnseignants():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        enseignants = cur.execute("SELECT * FROM Enseignant ORDER BY nom_enseignant, prenom_enseignant").fetchall()
        return render_template('A_infosEnseignants.html', enseignants=enseignants)
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))

### INFOS FAMILLE

@app.route('/infosFamilles', methods = ["GET"])
@login_required
def infosFamille():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        page_size = 10
        page = int(request.args.get('page', '1'))
        representants = cur.execute("SELECT * FROM Representant ORDER BY nom_representant, prenom_representant").fetchall()
        page_total = int(len(representants)/page_size) + 1
        return render_template('A_infosFamilles.html', representants=representants[((page-1) * page_size) : (page * page_size)], list_of_page = range(1, page_total + 1), page_total = page_total, page = page)
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))

### INFOS TARIFS

@app.route('/infosTarifs', methods = ["GET"])
@login_required
def infosTarifs():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        tarifs = cur.execute("SELECT * FROM tarif").fetchall()
        return render_template('A_infosTarifs.html', tarifs=tarifs)
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))

### LIAISON CLASSE

@app.route('/lierClasse/<int:code_ens>', methods=['GET', 'POST'])
@login_required
def lierClasse(code_ens):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        enseignant = cur.execute("SELECT nom_enseignant, prenom_enseignant, code_enseignant FROM Enseignant WHERE code_enseignant = ?", (code_ens, )).fetchone()
        enseignes = cur.execute("SELECT * FROM Enseigne WHERE code_enseignant = ?", (code_ens, )).fetchall()
        classes = cur.execute("SELECT * FROM Classe ORDER BY code_type, nom_classe").fetchall()
        if request.method == "POST":
            cur.execute("DELETE FROM Enseigne WHERE code_enseignant = ?", (code_ens, ))
            for classe in classes:
                if request.form.getlist(classe[1]):
                    cur.execute("INSERT INTO Enseigne VALUES (?,?)", (code_ens, classe[0],))
            db.commit()
            return redirect(url_for('detailsEnseignant', code_ens = code_ens))
        return render_template('A_lierClasse.html', enseignant = enseignant, classes = classes, enseignes = enseignes)
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))

### LIAISON ENSEIGNANT

@app.route('/lierEnseignant/<int:code_classe>', methods=['GET', 'POST'])
@login_required
def lierEnseignant(code_classe):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        enseignants = cur.execute("SELECT nom_enseignant, prenom_enseignant, code_enseignant FROM Enseignant").fetchall()
        enseignes = cur.execute("SELECT * FROM Enseigne WHERE code_classe = ?", (code_classe, )).fetchall()
        classe = cur.execute("SELECT * FROM Classe WHERE code_classe = ?", (code_classe, )).fetchone()
        if request.method == "POST":
            cur.execute("DELETE FROM Enseigne WHERE code_classe = ?", (code_classe, ))
            for enseignant in enseignants:
                nom = enseignant[0] + " " + enseignant[1]
                if request.form.getlist(nom):
                    cur.execute("INSERT INTO Enseigne VALUES (?,?)", (enseignant[2], code_classe,))
            db.commit()
            return redirect(url_for('detailsClasse', code_classe = code_classe))
        return render_template('A_lierEnseignant.html', enseignants = enseignants, classe = classe, enseignes = enseignes)
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))

### MODIFICATION MDP ENSEIGNANT

@app.route('/modifMDPE/<int:code_ens>', methods = ["GET"])
@login_required
def modifMDPE(code_ens):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        enseignant = cur.execute("SELECT identifiant FROM Enseignant WHERE code_enseignant = ?", (code_ens, )).fetchone()
        password = bcrypt.generate_password_hash("test")
        cur.execute("UPDATE Compte SET mot_de_passe = ? WHERE identifiant = ?", (password, enseignant[0], ))
        db.commit()
        return redirect(url_for('detailsEnseignant', code_ens = code_ens))
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))

### MODIFICATION MDP REPRESENTANT

@app.route('/modifMDPR/<int:code_rep>', methods = ["GET"])
@login_required
def modifMDPR(code_rep):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        representant = cur.execute("SELECT identifiant FROM Representant WHERE code_representant = ?", (code_rep, )).fetchone()
        password = bcrypt.generate_password_hash("test")
        cur.execute("UPDATE Compte SET mot_de_passe = ? WHERE identifiant = ?", (password, representant[0], ))
        db.commit()
        return redirect(url_for('detailsFamille', code_rep = code_rep))
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))

### SUPPRESSION CLASSE

@app.route('/suppressionC/<int:code_classe>', methods = ["GET"])
@login_required
def suppressionC(code_classe):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        enfants = cur.execute("SELECT * FROM Enfant WHERE code_classe = ?", (code_classe, )).fetchone()
        if not enfants:
            cur.execute("DELETE FROM Classe WHERE code_classe = ?", (code_classe, ))
            cur.execute("DELETE FROM Enseigne WHERE code_classe = ?", (code_classe, ))
            db.commit()
        return redirect(url_for('infosClasses'))
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))

### SUPPRESSION ENFANT

@app.route('/suppressionE/<int:code_enf>', methods = ["GET"])
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
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))

### SUPPRESSION ENSEIGNANT

@app.route('/suppressionEns/<int:code_ens>', methods =  ["GET"])
@login_required
def suppressionEns(code_ens):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        user = cur.execute("SELECT identifiant FROM Enseignant WHERE code_enseignant = ?", (code_ens, )).fetchone()
        cur.execute("DELETE FROM Compte WHERE identifiant = ?", (user[0], ))
        cur.execute("DELETE FROM Enseigne WHERE code_enseignant = ?", (code_ens, ))
        cur.execute("DELETE FROM Enseignant WHERE code_enseignant = ?", (code_ens, ))
        db.commit()
        return redirect(url_for('infosEnseignants'))
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))

### SUPPRESSION REPRESENTANT

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
        return redirect(url_for('infosFamille'))
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))

### SUPPRESSION TARIF

@app.route('/suppressionT/<int:code_tarif>', methods = ["GET"])
@login_required
def suppressionT(code_tarif):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Admin':
        enfants = cur.execute("SELECT * FROM Enfant WHERE code_tarif = ?", (code_tarif, )).fetchone()
        if not enfants:
            cur.execute("DELETE FROM Tarif WHERE code_tarif = ?", (code_tarif, ))
            db.commit()
        return redirect(url_for('infosTarifs'))
    if user[0] == 'Enseignant':
        return redirect(url_for('accueilEnseignant'))
    return redirect(url_for('accueil'))
