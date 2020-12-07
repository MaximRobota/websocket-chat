from .models import Users
from app import app, db
from .controllers.auth_controller import AuthController
from flask import jsonify
from flask import request
# from flask_login import login_required
# from flask_cors import CORS
# import os

# CORS(app, origins=[os.environ.get('CLIENT_HOST')])

auth_controller = AuthController()

# from flask import redirect
@app.before_first_request
def before_first_request_func():
    db.create_all()


@app.route('/')
def index():
    return 'identity-service is working!'


@app.route('/auth/register', methods=['POST'])
def register():
    return auth_controller.register(request.form)


@app.route('/auth/login', methods=['POST'])
def auth():
    return auth_controller.login(request.form)


@app.route('/auth/getIdByToken/<int:user_token>', methods=['GET'])
# @login_required
def get_id_by_token(user_token):
    return auth_controller.get_id_by_token(user_token)


# Display All users from database
@app.route('/users/', methods=['GET'])
# @login_required
def users():
    # data = cur.fetchall()
    # data = jsonify({'users': list(map(lambda users: users.serialize(), Users.query.all()))})
    # return render_template('index.html', data=data)
    return jsonify({'users': list(map(lambda users: users.serialize(), Users.query.all()))})


# # Route to Delete an user from the MySQL Database
@app.route('/users/<int:id>', methods=['DELETE'])
# @login_required
def delete(id):
    try:
        db.session.delete(Users.query.filter_by(id=id).first())
        db.session.commit()
        # return redirect('/users')
        return 'Deleted user #' + id
    except:
        return 'Error'
