from app import db
from datetime import datetime


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(80), unique=True)
    message = db.Column(db.String(80))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, uid, message):
        self.uid = uid
        self.message = message


    def serialize(self):
        return {"id": self.id,
                "uid": self.uid,
                "message": self.message,
                "created_on": self.created_on}