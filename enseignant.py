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

    

@app.route('/presence')
@login_required
def presence():
    db = get_db()
    cur = db.cursor() 
    now = datetime.datetime.today().strftime('%Y-%m-%d')
    user = cur.execute("SELECT type_compte FROM Compte WHERE identifiant = ?", (flask_login.current_user.name, )).fetchone()
    enfantsm=cur.execute("SELECT E.nom_enfant, E.prenom_enfant FROM Enseigne AS Ens INNER JOIN Enfant AS E ON Ens.code_classe = E.code_classe INNER JOIN Repas AS R ON R.code_enfant = E.code_enfant WHERE R.date_repas = ? ", (request.form("dates"),)).fetchall()
    classes=cur.execute("SELECT C.nom_classe FROM Classe AS C INNER JOIN Enseigne AS E ON E.code_classe=C.code_classe WHERE  E.code_enseigant=?").fetchall()
    return redirect(url_for('accueil'))
