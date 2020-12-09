from ..models import User
from app import app, db, bcrypt
from flask import request, make_response, jsonify
# from werkzeug.security import generate_password_hash, check_password_hash


class AuthController:

    def register(self, form):
        email = form['email']
        password = form['password']

        user = User.query.filter_by(email=email).first()
        if not user:
            try:
                user = User(
                    email=email,
                    password=password)
                    # password=generate_password_hash(password, method='sha256'))

                db.session.add(user)
                db.session.commit()
                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'auth_token': auth_token.decode(),
                    "meta": {
                        'status': 'success',
                        'message': 'Successfully registered.'
                    },
                    "user": {
                        'id': user.id,
                        'email': user.email
                    }
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                return {"error": f'Some error occurred. Please try again. {e}'}, 401

        return {"error": 'User already exists. Please Log in.'}, 202

    def login(self, form):
        email = form['email']
        password = form['password']

        try:
            user = User.query.filter_by(email=email).first()
            # if user or check_password_hash(user.password, password):
            if user or bcrypt.check_password_hash(user.password, password):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    return {
                                'auth_token': auth_token.decode(),
                                "user": user
                           }, 200
            else:
                return {"error": 'User does not exist.'}, 404

        except Exception as e:
            return {"error": f'Try again. {e}'}, 500

    def get_id_by_token(self, user_token):

        try:
            user = User.query.get(user_token)

            if not user:
                return {"error": 'Invalid token.'}, 403

            return {"user": user.id}
        except Exception as e:
            return {"error": str(e)}, 500

    def getUsers(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                responseObject = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'admin': user.admin,
                        'registered_on': user.registered_on
                    }
                }
                return make_response(jsonify(responseObject)), 200
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401


    # def logout(self):
    #     auth_header = request.headers.get('Authorization')
    #     if auth_header:
    #         auth_token = auth_header.split(" ")[1]
    #     else:
    #         auth_token = ''
    #     if auth_token:
    #         resp = User.decode_auth_token(auth_token)
    #         if not isinstance(resp, str):
    #             blacklist_token = BlacklistToken(token=auth_token)
    #             try:
    #                 # insert the token
    #                 db.session.add(blacklist_token)
    #                 db.session.commit()
    #                 responseObject = {
    #                     'status': 'success',
    #                     'message': 'Successfully logged out.'
    #                 }
    #                 return make_response(jsonify(responseObject)), 200
    #             except Exception as e:
    #                 responseObject = {
    #                     'status': 'fail',
    #                     'message': e
    #                 }
    #                 return make_response(jsonify(responseObject)), 200
    #         else:
    #             responseObject = {
    #                 'status': 'fail',
    #                 'message': resp
    #             }
    #             return make_response(jsonify(responseObject)), 401
    #     else:
    #         responseObject = {
    #             'status': 'fail',
    #             'message': 'Provide a valid auth token.'
    #         }
    #         return make_response(jsonify(responseObject)), 403

