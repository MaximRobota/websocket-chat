from .models import Users
from app import app, db
from flask import jsonify
from flask import request


# from flask import redirect

@app.route('/')
def index():
    return 'identity-service is working!'


@app.route('/user', methods=['POST'])
def new_user():
    name = request.form['name']
    password = request.form['password']
    user = Users(name=name, password=password)

    try:
        db.session.add(user)
        db.session.commit()
        return 'Added new user'
    except:
        return 'Error'


# Display All users from database
@app.route('/users/', methods=['GET'])
def users():
    # data = cur.fetchall()
    # data = jsonify({'users': list(map(lambda users: users.serialize(), Users.query.all()))})
    # return render_template('index.html', data=data)
    return jsonify({'users': list(map(lambda users: users.serialize(), Users.query.all()))})


# # Route to Delete an user from the MySQL Database
@app.route('/users/<int:id>', methods=['DELETE'])
def delete(id):
    try:
        db.session.delete(Users.query.filter_by(id=id).first())
        db.session.commit()
        # return redirect('/users')
        return 'Deleted user #' + id
    except:
        return 'Error'
