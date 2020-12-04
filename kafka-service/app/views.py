from app import app, db

@app.route('/')
def index():
    return 'kafka-service is working!'


