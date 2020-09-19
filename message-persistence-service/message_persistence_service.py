import mysql.connector
import yaml
# Show and create DB
db_conf = yaml.safe_load(open('db.yaml'))

mydb = mysql.connector.connect(
    host=db_conf['mysql_host'],
    user="root",
    password="root",
    database=db_conf['mysql_db']
)
mycursor = mydb.cursor()

mycursor.execute('SHOW DATABASES')
for db in mycursor:
    print(db)
# wrong
# if db_conf['mysql_db'] not in mycursor:
#     mycursor.execute('CREATE DATABASE ' + db_conf['mysql_db'])

##

from flask import Flask, jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.debug = True

# Bootstrap(app)
app.config['MYSQL_HOST'] = db_conf['mysql_host']
app.config['MYSQL_USER'] = db_conf['mysql_user']
app.config['MYSQL_PASSWORD'] = db_conf['mysql_password']
app.config['MYSQL_DB'] = db_conf['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/max_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

# Add the route to the Index page of the App
@app.route('/')
def index():
    return 'message-persistence-service'


# route to add New User
@app.route('/events', methods=['POST'])
def new_event():
    uid = request.form['uid']
    message = request.form['message']
    event = Events(uid=uid, message=message)
    try:
        db.session.add(event)
        db.session.commit()
        return 'Added new event'
    except:
        return 'Error'


# Display All events from database
@app.route('/events/', methods=['GET'])
def events():
    return jsonify({'events': list(map(lambda events: events.serialize(), Events.query.all()))})


# # Route to Delete an event from the MySQL Database
@app.route('/events/<int:id>', methods=['DELETE'])
def delete(id):
    try:
        db.session.delete(Events.query.filter_by(id=id).first())
        db.session.commit()
        return 'Deleted event #' + id
    except:
        return 'Error'

# Run the main App
if __name__ == '__main__':
    app.run(debug=True)


