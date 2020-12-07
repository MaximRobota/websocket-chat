from ..models import Users
from app import app, db
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash


class AuthController:

    def register(self, form):
        email = form['email']
        password = form['password']

        try:
            user = Users.query.filter_by(email=email).first()

            if user:
                return {"error": 'User exist'}, 500

            new_user = Users(email=email, password=generate_password_hash(password, method='sha256'))

            db.session.add(new_user)
            db.session.commit()

            return {"user": new_user.serialize()}
        except Exception as e:
            return {"error": str(e)}, 500

    def login(self, form):
        email = form['email']
        password = form['password']

        try:
            user = Users.query.filter_by(email=email).first()

            if not user or not check_password_hash(user.password, password):
                return {"error": 'Invalid login. Please check your login details and try again.'}, 403

            return {"id": user.serialize()}
        except Exception as e:
            return {"error": str(e)}, 500

    def get_id_by_token(self, user_token):

        try:
            user = Users.query.get(user_token)

            if not user:
                return {"error": 'Invalid token.'}, 403

            return {"user": user.id}
        except Exception as e:
            return {"error": str(e)}, 500
