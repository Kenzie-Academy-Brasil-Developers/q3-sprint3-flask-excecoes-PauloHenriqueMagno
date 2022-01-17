import os
from json import dump, load
from flask import jsonify, request
from app.excepts.bad_request_data_type_error import BadRequestDataTypeError
from app.excepts.conflict_email_error import ConflictEmailError

def check_or_create_database_file():
    data = {'data': []}

    if 'data' not in os.listdir('app'):
        os.system('mkdir ./app/data && touch ./app/data/database.json')
        with open('app/data/database.json', 'w') as file:
            dump(data, file, indent = 3)

    if 'database.json' not in os.listdir('app/data'):
        os.system('touch ./app/data/database.json')
        with open('app/data/database.json', 'w') as file:
            dump(data, file, indent = 3)

    if os.stat('app/data/database.json').st_size == 0:
        with open('app/data/database.json', 'w') as file:
            dump(data, file, indent = 3)
    
check_or_create_database_file()

def get_user_list():
    check_or_create_database_file()

    with open('app/data/database.json', 'r') as data:
        return jsonify(load(data)), 200

def create_user():
    try:
        check_or_create_database_file()

        with open('app/data/database.json', 'r') as data:
            database = load(data)

        user = dict(request.json)

        if type(user["name"]) != str or type(user["email"]) != str:
            raise BadRequestDataTypeError
        
        for any_user in database["data"]:
            if any_user["email"] == user["email"].lower():
                raise ConflictEmailError

        new_user = dict({})
        new_user["email"] = user["email"].lower()
        new_user["name"] = user['name'].title()
        
        if len(database["data"]) == 0:
            new_user["id"] =  1
        else:
            new_user["id"] = 1 + database["data"][len(database["data"])-1]["id"]

        database["data"].append(new_user)

        with open('app/data/database.json', 'w') as file:
            dump(database, file, indent = 3)
            
        return jsonify(database), 201
        
    except BadRequestDataTypeError:
        return jsonify({'message': 'Name and email must be string'}), 400

    except ConflictEmailError:
        return jsonify({'message': 'E-mail has already been taken'}), 409