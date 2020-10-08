from app import db
from datetime import datetime


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, name, password):
        self.name = name
        self.password = password


    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "message": self.password,
                "created_on": self.created_on}
