from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# todo: mettere qui le tabelle finali, le altre per testing sotto prossimo commento


class Utenti(db.Model, UserMixin):
    __tablename__ = 'utenti'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    cognome = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(256))  # todo : salt + password hanno un nome specifico , cercarlo e cambiare nome
    data_nascita = db.Column(db.Date())
    salt = db.Column(db.Integer, nullable=False)
    stud = db.relationship('Studenti', backref='Utenti', passive_deletes=True)
    prof = db.relationship('Professori', backref='Utenti', passive_deletes=True)


class Studenti(db.Model, UserMixin):
    id = db.Column(db.Integer, db.ForeignKey(Utenti.id, ondelete="CASCADE"), nullable=False, primary_key=True)
    scuola = db.Column(db.String(150))


class Professori(db.Model, UserMixin):
    id = db.Column(db.Integer, db.ForeignKey('utenti.id', ondelete="CASCADE"), nullable=False, primary_key=True)
    is_admin = db.Column(db.Boolean, default=False)


# todo: --- fine tabelle finali ---

'''
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)
        
'''
