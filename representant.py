from main import *

### ACTU 

@app.route('/actu', methods = ["GET"])
@login_required
def actu():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Representant':
        enfants = cur.execute("SELECT code_enfant, prenom_enfant FROM Enfant AS E INNER JOIN Representant AS R ON E.code_representant = R.code_representant WHERE R.identifiant = ? ORDER BY prenom_enfant", (flask_login.current_user.name, )).fetchall()
        return render_template('R_accueil.html', enfants = enfants)
    if user[0] == 'Admin':
        return redirect(url_for('accueilAdmin'))
    return redirect(url_for('accueilEnseignant'))

### AJOUT REPAS

@app.route('/ajoutRepas', methods = ["GET", "POST"])
@login_required
def ajoutRepas():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Representant':
        now = choixDate()
        newDate = now + datetime.timedelta(days = 2)
        enfants = cur.execute("SELECT code_enfant, prenom_enfant FROM Enfant AS E INNER JOIN Representant AS R ON E.code_representant = R.code_representant WHERE R.identifiant = ? ORDER BY prenom_enfant", (flask_login.current_user.name, )).fetchall()
        if request.method == "POST":
            date = datetime.datetime.strptime(request.form["repas"],'%Y-%m-%d')
            msg = None
            for enfant in enfants:
                if request.form.getlist(enfant[1]):
                    check = cur.execute("SELECT * FROM Repas WHERE date_repas = ? AND code_enfant = ? ", (date.strftime('%Y-%m-%d'), enfant[0], )).fetchone()
                    checkConge = cur.execute("SELECT * FROM Conge WHERE date_conge = ?", (date.strftime('%Y-%m-%d'),)).fetchone()
                    if not check and date >= newDate and checkConge == None:
                        cur.execute("INSERT INTO Repas(date_repas, code_enfant) VALUES (?,?)", (date.strftime('%Y-%m-%d'), enfant[0]))
                        msg = "Repas réservé avec succès"
                    if check:
                        msg = "Le repas est déjà réservé"
                    if date < newDate:
                        msg = "La date de réservation est de moins de 48h"
                    if checkConge:
                        msg = "Il n'y a pas école ce jour là"
            if msg == None:
                msg = "Aucun enfant sélectionné"
            db.commit()
            return render_template('R_ajoutRepas.html', enfants = enfants, now = now.strftime('%Y-%m-%d'), msg = msg)
        return render_template('R_ajoutRepas.html', enfants = enfants, now = now.strftime('%Y-%m-%d'))
    if user[0] == 'Admin':
        return redirect(url_for('accueilAdmin'))
    return redirect(url_for('accueilEnseignant'))

### ANNULATION REPAS 

@app.route('/annuleRepas/<int:code_repas>', methods = ["GET"])
@login_required
def annuleRepas(code_repas):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Representant':
        cur.execute("DELETE FROM Repas WHERE code_repas = ?", (code_repas, ))
        db.commit()
        return redirect(url_for('repas'))
    if user[0] == 'Admin':
        return redirect(url_for('accueilAdmin'))
    return redirect(url_for('accueilEnseignant'))

### DETAILS FACTURE

@app.route('/detailsFacture/<int:code_mois>', methods = ["GET"])
@login_required
def detailsFacture(code_mois):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Representant':
        now = choixDate().strftime('%d/%m/%Y')
        if code_mois < 10:
            code_mois = '0' + str(code_mois)
        else:
            code_mois = str(code_mois)
        if int(code_mois) < 13 and int(code_mois) > 7:
            year = str(choixDate().year - 1)
        else:
            year = str(choixDate().year)
        repas = cur.execute("SELECT R.date_repas, E.prenom_enfant, T.tarif FROM Repas AS R INNER JOIN Enfant AS E ON R.code_enfant = E.code_enfant "
        "INNER JOIN Representant AS Re ON Re.code_representant = E.code_representant INNER JOIN Tarif AS T ON E.code_tarif = T.code_tarif " 
        "WHERE Re.identifiant = ? AND strftime('%m', date_repas) = ? AND strftime('%Y', date_repas) = ? ORDER BY E.code_enfant, R.date_repas", (flask_login.current_user.name, code_mois, year, )).fetchall()
        dateInter = []
        for repa in repas:
            dateInter.append(datetime.datetime.strptime(repa[0], '%Y-%m-%d').strftime('%A %d/%m/%Y'))
        representant = cur.execute("SELECT nom_representant, prenom_representant, code_representant FROM Representant WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
        enfants = cur.execute("SELECT code_enfant, prenom_enfant FROM Enfant WHERE code_representant = ? ORDER BY prenom_enfant", (representant[2], )).fetchall()
        date = datetime.datetime(int(year), int(code_mois), 1).strftime('%Y%m')
        return render_template('R_detailsFacture.html', now = now, repas = repas, representant = representant, enfants = enfants, date = date, dateInter = dateInter)
    if user[0] == 'Admin':
        return redirect(url_for('accueilAdmin'))
    return redirect(url_for('accueilEnseignant'))

### ENFANT

@app.route('/enfant/<int:code_enfant>', methods = ["POST", "GET"])
@login_required
def enfant(code_enfant):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Representant':
        representant = cur.execute("SELECT code_representant FROM Representant WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
        enfant = cur.execute("SELECT nom_enfant, prenom_enfant, code_formule FROM Enfant WHERE code_representant = ? and code_enfant = ?", (representant[0], code_enfant, )).fetchone()
        enfants = cur.execute("SELECT code_enfant, prenom_enfant FROM Enfant WHERE code_representant = ? ORDER BY prenom_enfant", (representant[0], )).fetchall()
        formules = cur.execute("SELECT * FROM Formule").fetchall()
        joursManges = cur.execute("SELECT J.code_jour FROM Mange AS M INNER JOIN Jour AS J ON M.code_jour = J.code_jour WHERE M.code_enfant = ?", (code_enfant, )).fetchall()
        jours = cur.execute("SELECT * FROM Jour").fetchall()
        allergies = cur.execute("SELECT * FROM Allergie").fetchall()
        allergiques = cur.execute("SELECT code_allergie FROM EstAllergiqueA WHERE code_enfant = ?", (code_enfant, )).fetchall()
        now = choixDate()
        if request.method == "POST":
            cur.execute("DELETE FROM Mange WHERE code_enfant = ?", (code_enfant, ))
            cur.execute("DELETE FROM EstAllergiqueA WHERE code_enfant = ?", (code_enfant, ))
            for allergie in allergies:
                if request.form.getlist(allergie[1]):
                    cur.execute("INSERT INTO EstAllergiqueA VALUES (?,?)", (allergie[0], code_enfant,))
            i = 0
            for jour in jours:
                if request.form.getlist(jour[1]):
                    cur.execute("INSERT INTO Mange VALUES (?,?)", (jour[0], code_enfant, ))
                    formule(jour[0], int(now.year), code_enfant)
                    i += 1
            if i == 0:
                i = 5
            cur.execute("UPDATE Enfant SET code_formule = ? WHERE code_enfant = ?", (i, code_enfant, ))

            db.commit()
            enfant = cur.execute("SELECT nom_enfant, prenom_enfant, code_formule FROM Enfant WHERE code_representant = ? and code_enfant = ?", (representant[0], code_enfant, )).fetchone()
            joursManges = cur.execute("SELECT J.code_jour FROM Mange AS M INNER JOIN Jour AS J ON M.code_jour = J.code_jour WHERE M.code_enfant = ?", (code_enfant, )).fetchall()
            allergiques = cur.execute("SELECT code_allergie FROM EstAllergiqueA WHERE code_enfant = ?", (code_enfant, )).fetchall()
        return render_template('R_enfant.html', enfants = enfants, enfant = enfant, formules = formules, jours = jours, joursManges = joursManges, allergies = allergies, allergiques = allergiques)
    if user[0] == 'Admin':
        return redirect(url_for('accueilAdmin'))
    return redirect(url_for('accueilEnseignant'))

### FACTURE

@app.route('/facture', methods = ["GET", "POST"])
@login_required
def facture():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Representant':
        months = ["Aout","Septembre","Octobre","Novembre","Décembre","Janvier","Février","Mars","Avril","Mai","Juin","Juillet"]
        year = choixDate().year
        year1 = year - 1
        mois = choixDate().month
        enfants = cur.execute("SELECT code_enfant, prenom_enfant FROM Enfant AS E INNER JOIN Representant AS R ON E.code_representant = R.code_representant WHERE R.identifiant = ? ORDER BY prenom_enfant", (flask_login.current_user.name, )).fetchall()
        if request.method == "POST":
            return redirect(url_for('detailsFacture', code_mois = request.form["facture"]))
        return render_template('R_facture.html', year = year, months = months, mois = mois ,year1 = year1, enfants = enfants)
    if user[0] == 'Admin':
        return redirect(url_for('accueilAdmin'))
    return redirect(url_for('accueilEnseignant'))

### INFO 1

@app.route('/info', methods = ["GET"])
@login_required
def info():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Representant':
        info = cur.execute("SELECT * FROM Representant WHERE identifiant = ?",(flask_login.current_user.name, )).fetchone()
        compte = cur.execute("SELECT * from Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
        enfants = cur.execute("SELECT code_enfant, prenom_enfant FROM Enfant AS E INNER JOIN Representant AS R ON E.code_representant = R.code_representant WHERE R.identifiant = ? ORDER BY prenom_enfant", (flask_login.current_user.name, )).fetchall()
        return render_template('R_info.html', info = info, compte = compte, enfants = enfants)
    if user[0] == 'Admin':
        return redirect(url_for('accueilAdmin'))
    return redirect(url_for('accueilEnseignant'))

### INFO 2

@app.route('/info2', methods = ["GET", "POST"])
@login_required
def info2():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Representant':
        info = cur.execute("SELECT * FROM Representant WHERE identifiant = ?",(flask_login.current_user.name, )).fetchone()
        enfants = cur.execute("SELECT code_enfant, prenom_enfant FROM Enfant AS E INNER JOIN Representant AS R ON E.code_representant = R.code_representant WHERE R.identifiant = ? ORDER BY prenom_enfant", (flask_login.current_user.name, )).fetchall()
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
    if user[0] == 'Admin':
        return redirect(url_for('accueilAdmin'))
    return redirect(url_for('accueilEnseignant'))


### INFO 3

@app.route('/info3', methods = ["GET", "POST"])
@login_required
def info3():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Representant':
        info = cur.execute("SELECT * FROM Representant WHERE identifiant = ?",(flask_login.current_user.name, )).fetchone()
        enfants = cur.execute("SELECT code_enfant, prenom_enfant FROM Enfant AS E INNER JOIN Representant AS R ON E.code_representant = R.code_representant WHERE R.identifiant = ? ORDER BY prenom_enfant", (flask_login.current_user.name, )).fetchall()
        if request.method== "POST": 
            user = cur.execute("SELECT * FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
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
    if user[0] == 'Admin':
        return redirect(url_for('accueilAdmin'))
    return redirect(url_for('accueilEnseignant'))

### INSCRIPTION

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
    
### MENUS

@app.route('/menus', methods = ["GET"])
@login_required
def menus():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Representant':
        enfants = cur.execute("SELECT code_enfant, prenom_enfant FROM Enfant AS E INNER JOIN Representant AS R ON E.code_representant = R.code_representant WHERE R.identifiant = ? ORDER BY prenom_enfant", (flask_login.current_user.name, )).fetchall()
        return render_template('R_menu.html', enfants = enfants)
    if user[0] == 'Admin':
        return redirect(url_for('accueilAdmin'))
    return redirect(url_for('accueilEnseignant'))

### REPAS

@app.route('/repas', methods = ["GET", "POST"])
@login_required
def repas():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Representant':
        code_rep = cur.execute("SELECT code_representant FROM Representant WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
        enfants = cur.execute("SELECT code_enfant, prenom_enfant, nom_enfant FROM Enfant WHERE code_representant = ? ORDER BY prenom_enfant", (code_rep[0], )).fetchall()
        repas = []
        year = choixDate().year
        year1 = year - 1
        mois = choixDate().month
        now = choixDate()
        months = listeMois(mois)
        new_dateB = datetime.datetime(year, int(now.month), now.day)
        lastDay = last_day_of_month(new_dateB)
        new_dateE = datetime.datetime(year, int(now.month), lastDay.day)
        limit = int(now.day) + 2
        date_limite = now.replace(day = limit)
        if request.method == "POST":
            code_mois = index(request.form["repas"])
            if code_mois < 13 and code_mois > 7:
                year = int(choixDate().year - 1)
            else:
                year = int(choixDate().year)
            if request.form["repas"] == months[0]:
                day = now.day
            else:
                day = 1
            new_dateB = datetime.datetime(year, code_mois, day)
            lastDay = last_day_of_month(new_dateB)
            new_dateE = datetime.datetime(year, code_mois, lastDay.day)
            mois = request.form["repas"]
        dateInter = []
        for enfant in enfants:
            repas.append(cur.execute("SELECT * FROM Repas WHERE code_enfant = ? AND date_repas >= ? AND date_repas <= ? ORDER BY date_repas", (enfant[0], new_dateB.strftime('%Y-%m-%d') , new_dateE.strftime('%Y-%m-%d'), )).fetchall())
        for repasEnfants in repas:
            for repa in repasEnfants:
                dateInter.append(datetime.datetime.strptime(repa[1], '%Y-%m-%d').strftime('%A %d/%m/%Y'))
        return render_template('R_repas.html', enfants = enfants, repasEnfants = repas, date_limite = date_limite.strftime('%A %d/%m/%Y'), date_annulation = date_limite.strftime('%Y-%m-%d'), year = year, months = months, mois = mois ,year1 = year1, dateInter = dateInter)
    if user[0] == 'Admin':
        return redirect(url_for('accueilAdmin'))
    return redirect(url_for('accueilEnseignant'))

### FONCTIONS UTILES POUR LES DIFFERENTS PAGES

def formule(idJour, annee, code_enfant):
    db = get_db()
    cur = db.cursor()
    now = choixDate()
    anneeBis = annee
    if now.month > 7:
        anneeBis += 1
    debut = datetime.datetime(annee, now.month, now.day).strftime('%m/%d/%Y')
    fin = datetime.datetime(anneeBis, 7, 15).strftime('%m/%d/%Y')
    if idJour == 1:
        dates = pd.date_range(start=debut, end=fin, freq='W-MON').strftime('%Y-%m-%d').tolist()
    if idJour == 2:
        dates = pd.date_range(start=debut, end=fin, freq='W-TUE').strftime('%Y-%m-%d').tolist()
    if idJour == 3:
        dates = pd.date_range(start=debut, end=fin, freq='W-THU').strftime('%Y-%m-%d').tolist()
    if idJour == 4:
        dates = pd.date_range(start=debut, end=fin, freq='W-FRI').strftime('%Y-%m-%d').tolist()
    conges = cur.execute("SELECT date_conge FROM Conge ORDER BY date_conge").fetchall()
    repas = cur.execute("SELECT date_repas FROM Repas WHERE code_enfant = ?", (code_enfant, )).fetchall()
    print(conges)
    print(dates)
    find = False
    for date in dates:
        for repa in repas:
            if date == repa[0]:
                find = True
        for conge in conges:
            if date == conge[0]:
                find = True
        if not find:
            cur.execute("INSERT INTO Repas(date_repas, code_enfant) VALUES (?,?)", (date, code_enfant,))
        find = False
    return


### Utilisé dans repas, permet d'avoir le numéro du mois associé
def index(mois):
    if mois == "Janvier":
        return 1
    if mois == "Février":
        return 2
    if mois == "Mars":
        return 3
    if mois == "Avril":
        return 4
    if mois == "Mai":
        return 5
    if mois == "Juin":
        return 6
    if mois == "Juillet":
        return 7
    if mois == "Aout":
        return 8
    if mois == "Septembre":
        return 9
    if mois == "Octobre":
        return 10
    if mois == "Novembre":
        return 11
    if mois == "Décembre":
        return 12
    
        
### Utilisé dans Repas, permet de connaitre la derniere date d'un mois
def last_day_of_month(any_day):
    # this will never fail
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
    return next_month - datetime.timedelta(days=next_month.day)

### Utilisé dans Repas pour avoir la liste des futurs en mois en focntion du mois actuel
def listeMois(mois):
    if mois == 1:
        months = ["Janvier","Février","Mars","Avril","Mai","Juin","Juillet"]
    if mois == 2:
        months = ["Février","Mars","Avril","Mai","Juin","Juillet"]
    if mois == 3:
        months = ["Mars","Avril","Mai","Juin","Juillet"]
    if mois == 4:
        months = ["Avril","Mai","Juin","Juillet"]
    if mois == 5:
        months = ["Mai","Juin","Juillet"]
    if mois == 6:
        months = ["Juin","Juillet"]
    if mois == 7:
        months = ["Juillet"]
    if mois == 8:
        months = ["Aout","Septembre","Octobre","Novembre","Décembre","Janvier","Février","Mars","Avril","Mai","Juin","Juillet"]
    if mois == 9:
        months = ["Septembre","Octobre","Novembre","Décembre","Janvier","Février","Mars","Avril","Mai","Juin","Juillet"]
    if mois == 10:
        months = ["Octobre","Novembre","Décembre","Janvier","Février","Mars","Avril","Mai","Juin","Juillet"]
    if mois == 11:
        months = ["Novembre","Décembre","Janvier","Février","Mars","Avril","Mai","Juin","Juillet"]
    if mois == 12:
        months = ["Décembre","Janvier","Février","Mars","Avril","Mai","Juin","Juillet"]
    return months


