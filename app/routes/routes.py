from app import app
from flask import jsonify, url_for, redirect, session, render_template, request, flash
from ..views import users
from ..views import meli
import requests, json

@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'Hello World!'})

@app.route('/users', methods=['GET'])
def get_users():
    return users.get_users()

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    return users.get_user(id)

@app.route('/users', methods=['POST'])
def post_users():
    return users.post_user()

@app.route('/users/<id>', methods=['DELETE'])
def delete_users(id):
    return users.delete_user(id)

@app.route('/users/<id>', methods=['PUT'])
def update_users(id):
    return users.update_user(id)

@app.route('/user/login', methods=['POST'])
def login_user():
    return users.login_user()

@app.route('/authorization/', methods=['GET'])
def update_code():
    return meli.update_code()

@app.route('/meli/shipment/<id>', methods=['GET'])
def meli_shipments_id(id):
    return meli.meli_shipments_items(id)

@app.route('/meli/item/<id>', methods=['GET'])
def meli_item_id(id):
    return meli.meli_item_id(id)