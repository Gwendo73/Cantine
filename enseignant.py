from datetime import date
from main import *

@app.route('/accueilEnseignant')
@login_required
def accueilEnseignant():
    db = get_db()
    cur = db.cursor() 
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Enseignant':
        infos= cur.execute("SELECT * FROM Enseignant WHERE identifiant=?",(flask_login.current_user.name, )).fetchone()
        return render_template('E_accueilEnseignant.html', infos=infos)
    if user[0] == 'Admin':
        return redirect(url_for('accueilAdmin'))
    return redirect(url_for('accueil'))

@app.route('/modifmdp', methods = ["GET", "POST"] )
@login_required
def modifmdp():
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Enseignant':
        infos = cur.execute("SELECT * FROM Enseignant WHERE identifiant=?",(flask_login.current_user.name, )).fetchone()
        if request.method== "POST": 
            user = cur.execute("SELECT * FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
            if user: 
                new_user = User(user[0], user[1])
                if bcrypt.check_password_hash(new_user.password, request.form["fpassword"]):
                    if bcrypt.check_password_hash(new_user.password, request.form["password"]):
                        error = 'Vous ne pouvez pas réutiliser un ancien mot de passe'
                        return render_template('E_modifInfosmdp.html', error = error, infos=infos)

                    if request.form["password"] == request.form["password2"]:
                        password = bcrypt.generate_password_hash(request.form["password"])
                        cur.execute("UPDATE Compte SET mot_de_passe = ? WHERE identifiant = ?", (password, flask_login.current_user.name, ))
                        db.commit()
                        return redirect(url_for('info'))

                    error = "Le mot de passe n'est pas le même"
                    return render_template('E_modifInfosmdp.html', error = error, infos=infos)

                else :
                    error = "Le mot de passe n'est pas le bon"
                    return render_template("E_modifInfosmdp.html", error=error, infos=infos)
                    
        return render_template('E_modifInfosmdp.html', infos = infos)
    if user[0] == 'Admin':
        return redirect(url_for('accueilAdmin'))
    return redirect(url_for('accueil'))

    

@app.route('/presence', defaults={'code_classe': 0},methods = ["POST", "GET"])
@app.route('/presence/<int:code_classe>', methods = ["POST", "GET"])
@login_required
def presence(code_classe):
    db = get_db()
    cur = db.cursor() 
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Enseignant':
        allergies = []
        now = choixDate().strftime('%Y-%m-%d')
        nowJolie = choixDate().strftime('%A %d %B')
        user = cur.execute("SELECT code_enseignant FROM Enseignant WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
        classes = cur.execute("SELECT C.code_classe, C.nom_classe FROM Classe AS C INNER JOIN Enseigne AS E ON E.code_classe = C.code_classe WHERE E.code_enseignant = ?", (user[0],)).fetchall()
        if code_classe == 0:
            code = classes[0][0]
        else:
            code = code_classe
        enfants = cur.execute("SELECT E.nom_enfant, E.prenom_enfant, E.code_enfant, Rep.telephone, R.code_repas FROM Enseigne AS Ens INNER JOIN Enfant AS E ON Ens.code_classe = E.code_classe INNER JOIN Repas AS R ON R.code_enfant = E.code_enfant INNER JOIN Representant AS Rep ON Rep.code_representant = E.code_representant WHERE R.date_repas = ? AND E.code_classe = ? ORDER BY E.nom_enfant, E.prenom_enfant", (now, code, )).fetchall()
        classeActuelle = cur.execute("SELECT C.code_classe, C.nom_classe FROM Classe AS C INNER JOIN Enseigne AS E ON E.code_classe = C.code_classe WHERE E.code_enseignant = ? AND C.code_classe = ?", (user[0], code, )).fetchone()
        for enfant in enfants:
            allergies.append(cur.execute("SELECT Al.nom_allergie, A.code_enfant FROM EstAllergiqueA AS A INNER JOIN Allergie AS Al ON Al.code_allergie = A.code_allergie WHERE A.code_enfant = ?", (enfant[2], )).fetchall())
        if request.method == "POST":
            allergies = []
            now = request.form["calendar"]
            nowJolie = datetime.datetime.strptime(request.form["calendar"], '%Y-%m-%d').strftime('%A %d %B')
            classes = cur.execute("SELECT C.code_classe, C.nom_classe FROM Classe AS C INNER JOIN Enseigne AS E ON E.code_classe = C.code_classe WHERE E.code_enseignant = ?", (user[0], )).fetchall()
            classeActuelle = cur.execute("SELECT C.code_classe, C.nom_classe FROM Classe AS C INNER JOIN Enseigne AS E ON E.code_classe = C.code_classe WHERE E.code_enseignant = ? AND C.code_classe = ?", (user[0], request.form["classe"], )).fetchone()
            enfants = cur.execute("SELECT E.nom_enfant, E.prenom_enfant, E.code_enfant, Rep.telephone, R.code_repas FROM Enseigne AS Ens INNER JOIN Enfant AS E ON Ens.code_classe = E.code_classe INNER JOIN Repas AS R ON R.code_enfant = E.code_enfant INNER JOIN Representant AS Rep ON Rep.code_representant=E.code_representant WHERE R.date_repas = ? AND E.code_classe = ? ORDER BY nom_enfant, prenom_enfant ", (now, classeActuelle[0])).fetchall()           
            for enfant in enfants:
                allergies.append(cur.execute("SELECT Al.nom_allergie, A.code_enfant FROM EstAllergiqueA AS A INNER JOIN Allergie AS Al ON Al.code_allergie = A.code_allergie WHERE A.code_enfant = ?", (enfant[2], )).fetchall())
        print(enfants)
        return render_template("E_presence.html", classes = classes, enfants = enfants, now = now, allergiesEnfants = allergies, classeActuelle = classeActuelle, nowJolie = nowJolie)
    if user[0] == 'Admin':
        return redirect(url_for('accueilAdmin'))
    return redirect(url_for('accueil'))

@app.route('/supprRepas/<int:code_repas>', methods=["GET"])
@login_required
def supprRepas(code_repas):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Enseignant':
        classe = cur.execute("SELECT E.code_classe FROM Enfant AS E INNER JOIN Repas AS R ON R.code_enfant = E.code_enfant WHERE R.code_repas = ?", (code_repas, )).fetchone()
        cur.execute("DELETE FROM Repas WHERE code_repas = ?", (code_repas, ))
        db.commit()
        return redirect(url_for('presence', code_classe = classe[0]))
    if user[0] == 'Admin':
        return redirect(url_for('accueilAdmin'))
    return redirect(url_for('accueil'))

@app.route('/supprAll/<int:code_classe>/<date>', methods=["GET"])
@login_required
def supprAll(code_classe, date):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    if user[0] == 'Enseignant':
        enfants = cur.execute("SELECT code_enfant FROM Enfant WHERE code_classe = ?", (int(code_classe),)).fetchall()
        for enfant in enfants:
            cur.execute("DELETE FROM Repas WHERE code_enfant = ? and date_repas = ?", (enfant[0], date, ))
        #db.commit()
        return redirect(url_for('presence', code_classe = int(code_classe)))
    if user[0] == 'Admin':
        return redirect(url_for('accueilAdmin'))
    return redirect(url_for('accueil'))
    
