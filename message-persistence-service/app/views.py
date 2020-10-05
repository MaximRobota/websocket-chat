from flask import jsonify
from flask import request
from app import app, db
from .models import Events

@app.route('/')
def index():
    return 'message-persistence-service'

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