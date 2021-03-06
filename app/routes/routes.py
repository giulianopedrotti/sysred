from app import app
from flask import jsonify, url_for, redirect, session, render_template, request, flash
from ..views import users
from ..views import meli
from ..views import sige
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

@app.route('/meli/order/<id>', methods=['GET'])
def meli_order_id(id):
    return meli.meli_order_id(id)

@app.route('/meli/inova/<id>', methods=['GET'])
def meli_inova_id(id):
    return meli.meli_inova_id(id)

@app.route('/meli/inova/<id>/items', methods=['GET'])
def meli_inova_items(id):
    return meli.meli_inova_id(id,fil="items")

@app.route('/meli/inova/<id>/info', methods=['GET'])
def meli_inova_info(id):
    return meli.meli_inova_id(id,fil="info")

@app.route('/meli/inova/<id>/questions', methods=['GET'])
def meli_inova_questions(id):
    return meli.meli_inova_id(id,fil="questions")

@app.route('/meli/inova/<id>/messages', methods=['GET'])
def meli_inova_messages(id):
    return meli.meli_inova_id(id,fil="messages")

@app.route('/meli/inova/<id>/payments', methods=['GET'])
def meli_inova_payments(id):
    return meli.meli_inova_id(id,fil="payments")

@app.route('/sige/estoque/<deposito>', methods=['GET'])
def sige_deposito_estoque(deposito):
    return sige.sige_deposito_estoque(deposito)

@app.route('/sige/pedidos/pesquisar/<parameter>/<value>/<findvalue>', methods=['GET'])
def sige_pedidos_pesquisar(parameter, value, findvalue):
    return sige.sige_pedidos_pesquisar(parameter, value, findvalue)

@app.route('/order', methods=['POST'])
def sige_post_order():
    return sige.sige_post_order()