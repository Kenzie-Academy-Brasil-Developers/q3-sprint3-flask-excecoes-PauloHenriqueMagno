from flask import Flask
from app.services.users.users import get_user_list, create_user

app = Flask(__name__)

@app.get('/user')
def get_users():
    return get_user_list()

@app.post('/user')
def create_new_user():
    return create_user()