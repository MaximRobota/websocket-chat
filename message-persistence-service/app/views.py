from app import app, db

@app.route('/')
def index():
    return 'message-persistence-service is working!'


