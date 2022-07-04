from MySQLdb import IntegrityError
from werkzeug.security import generate_password_hash,check_password_hash
from app import db, app
from flask import request, jsonify
from ..models.users import Users, user_schema, users_schema

"""Retorna lista de usuários"""


def get_users():
    name = request.args.get('name')
    username = request.args.get('username')
    authorization = request.headers.get('Authorization')
    if authorization != (app.config['AUTHORIZATION']):
        return jsonify({'message': "unauthorized access"}), 401
    if name:
        users = Users.query.filter(Users.name.like(f'%{name}%')).all()
    elif username:
        users = Users.query.filter(Users.username.like(f'%{username}%')).all()
    else:
        users = Users.query.all()
    if users:
        result = users_schema.dump(users)
        return jsonify({'message': 'successfully fetched', 'data': result})

    return jsonify({'message': 'nothing found', 'data': {}})


"""Valida usuário e senha"""
def login_user():
    authorization = request.headers.get('Authorization')
    if authorization != (app.config['AUTHORIZATION']):
        return jsonify({'message': "unauthorized access"}), 401
    username = request.json['username']
    password = request.json['password']
    user = user_by_username(username)
    if user:
        result = user_schema.dump(user)
        passwd = check_passwd(result['password'],password)
        if passwd:
            return jsonify({'message': 'credential valid', 'username': username, 'password': passwd})
        else:
            return jsonify({'message': 'credential invalid', 'username': username, 'password': passwd})
    
    return jsonify({'message': "credential don't validate"}), 404

"""Retorna usuário específico pelo ID no parametro da request"""


def get_user(id):
    authorization = request.headers.get('Authorization')
    if authorization != (app.config['AUTHORIZATION']):
        return jsonify({'message': "unauthorized access"}), 401
    user = Users.query.get(id)
    if user:
        result = user_schema.dump(user)
        return jsonify({'message': 'successfully fetched', 'data': result}), 201

    return jsonify({'message': "user don't exist", 'data': {}}), 404


"""Cadastro de usuários com validação de existência"""


def post_user():
    username = request.json['username']
    password = request.json['password']
    name = request.json['name']
    email = request.json['email']
    admin = True

    authorization = request.headers.get('Authorization')
    if authorization != (app.config['AUTHORIZATION']):
        return jsonify({'message': "unauthorized access"}), 401

    user = user_by_username(username)
    if user:
        result = user_schema.dump(user)
        return jsonify({'message': 'user already exists', 'data': result})

    pass_hash = generate_password_hash(password)
    user = Users(username, pass_hash, name, email,admin)

    try:
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user)
        if "data" in result:
            return jsonify({'message': 'successfully registered', 'data': result.data}), 201
        else:
            return jsonify({'message': 'creation process in progess', 'data': result})
    except Exception as e:
        print(e)
        return jsonify({'message': 'unable to create', 'data': {}}), 500
    finally:
        db.session.close()


"""Atualiza usuário baseado no ID, caso o mesmo exista."""


def update_user(id):
    username = request.json['username']
    password = request.json['password']
    name = request.json['name']
    email = request.json['email']
    db.session.rollback()
    user = Users.query.get(id)

    if not user:
        return jsonify({'message': "user don't exist", 'data': {}}), 404

    pass_hash = generate_password_hash(password)

    if user:
        try:
            user.username = username
            user.password = pass_hash
            user.name = name
            user.email = email
            db.session.commit()
            result = user_schema.dump(user)
            return jsonify({'message': 'successfully updated', 'data': result.data}), 201
        except:
            return jsonify({'message': 'unable to update', 'data':{}}), 500


"""Deleta usuário com base no ID da request"""


def delete_user(id):
    user = Users.query.get(id)
    if not user:
        return jsonify({'message': "user don't exist", 'data': {}}), 404

    if user:
        try:
            db.session.delete(user)
            result = user_schema.dump(user)
            return jsonify({'message': 'successfully deleted', 'data': result}), 200
        except:
            return jsonify({'message': 'unable to delete', 'data': {}}), 500


def user_by_username(username):
    try:
        return Users.query.filter(Users.username == username).one()
    except:
        return None

def check_passwd(cryptpasswd,password):
    try:
        if check_password_hash(cryptpasswd, password):
            return True
        else:
            return False
    except:
        return False
