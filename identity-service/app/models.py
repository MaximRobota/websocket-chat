from app import db
from datetime import datetime


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, email, password):
        self.email = email
        self.password = password


    def serialize(self):
        return {"id": self.id,
                "email": self.email,
                "password": self.password,
                "created_on": self.created_on}
