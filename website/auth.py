from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import Utenti, Studenti, Professori
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        utente = Utenti.query.filter_by(email=email).first()
        if utente:  # se esiste in db
            if check_password_hash(utente.password, password):  # se pwd coincide
                flash("Logged in!", category='success')
                doc = Professori.query.filter_by(email=email).first()  # controllo se prof
                if doc:  # se professore
                    if doc.is_admin:  # ramo amministratore todo:da fare
                        # reindirizzo a schermata admin
                        login_user(utente, remember=True)
                        return redirect(url_for('views.home'))
                    else:  # ramo professore todo: da fare
                        login_user(utente, remember=True)
                        return redirect(url_for('views.home'))
                else:  # ramo studente todo: da fare
                    login_user(utente, remember=True)
                    return redirect(url_for('views.home'))
            else:
                flash('Combinazione email passowrd errata', category='error')
        else:
            flash('Combinazione email passowrd errata', category='error')

    return render_template("login.html", user=current_user)


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        nome = request.form.get("nome")
        cognome = request.form.get("cognome")
        email = request.form.get("email")
        password = request.form.get("password")
        password1 = request.form.get("password1")
        data_nascita = request.form.get("data_nascita")
        salt = 1  # todo: pensare a come creare il salt
        scuola = request.form.get("scuola")
        email_exists = Utenti.query.filter_by(email=email).first()

        if email_exists:
            flash('Email già in uso.', category='error')
        elif password != password1:
            flash('Password non combaciano', category='error')
        elif len(password) < 1:
            flash('Password troppo corta.', category='error')
        elif len(email) < 4:
            flash("Email non valida.", category='error')
        else:

            new_user = Utenti(nome=nome, cognome=cognome, email=email, password=generate_password_hash(
                password, method='sha256'), data_nascita=data_nascita, salt=salt)
            new_studente = Studenti(id=new_user.id, scuola=scuola)
            db.session.add(new_user)
            db.session.add(new_studente)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))
