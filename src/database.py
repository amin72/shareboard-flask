from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now())

    tickets = db.relationship('Ticket', backref='user')

    def __str__(self):
        return f'User: {self.username}'


class Ticket(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.Text(), nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __str__(self) -> str:
        return f'Ticket: {self.user_id.username}'