# -----------------------------------
#      Sige View
# -----------------------------------
from app import db, app
from app.views.meli import meli_refresh_token, token_by_userid
from flask import request, jsonify
import requests, json
from datetime import datetime, timedelta

"""Recebe a quantidade em estoque de produtos"""
def sige_api(path, context):
    sige_resource = path + context
    sige_headers = {
        'Accept': 'application/json',
        'Authorization-Token': app.config['SIGE_TOKEN'],
        'User': app.config['SIGE_USER'],
        'App': app.config['SIGE_APP']
    }
    sige_request = requests.get(
        app.config['SIGE_URL'] + sige_resource, headers=sige_headers)
    #Return Json Format
    return json.loads(sige_request.content.decode('utf-8'))

"""Recebe a quantidade em estoque de produtos"""

def sige_deposito_estoque(deposito):
    authorization = request.headers.get('Authorization')
    if authorization != (app.config['AUTHORIZATION']):
        return jsonify({'message': "unauthorized access"}), 401
    sige_json = sige_api("/request/Estoque/","BuscarQuantidades?deposito=" + deposito)
    try:
        return jsonify(sige_json['EstoqueItens']),200
    except:
        return jsonify({'message': "error to fecthed items"}), 500