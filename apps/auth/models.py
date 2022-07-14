from database import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password

    def __repr__(self):
        return f"<User {self.name}>"
