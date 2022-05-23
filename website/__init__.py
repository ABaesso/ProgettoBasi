from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/basi22'
    # jdbc:postgresql://localhost:5432/postgres    postgresql://postgres:password@localhost/basi22
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = "helloworld"
    app.secret_key = 'helloworld'
    db = SQLAlchemy(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import Utenti

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # todo : cambiare in utenti per fare accesso senza chiamare studenti e docenti

        return Utenti.query.get(int(id))

    return app


def create_database(app):
    db.create_all(app=app)
    print("Created database!")
