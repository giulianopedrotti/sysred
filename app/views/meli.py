from app import db, app
from flask import request, jsonify
from ..models.meli import Meli, meli_schema, melis_schema
import requests,json
from datetime import datetime, timedelta

"""Recebe o code de autorization e insere no banco"""

def update_code():
    code = request.args.get("code")
    meli_code = token_by_code(code)
    meli_url = app.config['MELI_URL']
    meli_client_id = app.config['MELI_CLIENT_ID']
    meli_client_secret = app.config['MELI_CLIENT_SECRET']
    meli_redirect_uri = app.config['MELI_REDIRECT_URI']
    login = meli_login(meli_url, meli_client_id, meli_client_secret, code, meli_redirect_uri )
    login_result = json.loads(login)

    if meli_code:
        try:
            meli_code.meli_code = code
            return jsonify({'message': 'successfully updated'}), 201
        except:
            return jsonify({'message': 'unable to update'}), 500
    elif not "error" in login:
        try:
            access_token = login_result['access_token']
            token_type = login_result['token_type']
            expires_in = login_result['expires_in']
            expires_datetime = datetime.now() + timedelta(seconds=expires_in)
            scope = login_result['scope']
            user_id = login_result['user_id']
            refresh_token = login_result['refresh_token']
            meli = token_by_userid(user_id)
            if meli:
                meli.access_token = access_token
                meli.token_type = token_type
                meli.expires_in = expires_in
                meli.expires_datetime = expires_datetime
                meli.scope = scope
                meli.user_id = user_id
                meli.refresh_token = refresh_token
            else:
                meli = Meli(code,access_token, token_type, expires_in, expires_datetime, scope, user_id, refresh_token)
                db.session.add(meli)
            db.session.commit()
            result = meli_schema.dump(meli)
            return jsonify({'message': 'successfully registered', 'data': result.data}), 201
        except:
            return jsonify({'message': 'unable to create'}), 500
    else:
        return jsonify(login_result), 400

def token_by_code(code):
    try:
        return Meli.query.filter(Meli.meli_code == code).one()
    except:
        return None

def token_by_userid(userid):
    try:
        return Meli.query.filter(Meli.user_id == userid).one()
    except:
        return None

def meli_login(meli_url, meli_client_id, meli_client_secret, meli_code, meli_redirect_uri):
    meli_data = {
        'grant_type': 'authorization_code',
        'client_id': meli_client_id,
        'client_secret': meli_client_secret,
        'code': meli_code,
        'redirect_uri': meli_redirect_uri
    }
    meli_params = (
        ('response_type', 'code'),
    )
    meli_response = requests.post(
        meli_url, params=meli_params, data=meli_data)
    print(meli_response.status_code)
    print(meli_response.content)
    # Return Json Format
    return meli_response.content.decode('utf-8')

def meli_refresh_token(app_id, secret_key, refresh_token):
    _meli_refresh_token_resource = "/oauth/token?grant_type=refresh_token&client_id=" + app_id + "&client_secret=" + secret_key + "&refresh_token=" + refresh_token
    _meli_refresh_token_request = requests.post(app.config['MELI_API_URI'] + _meli_refresh_token_resource)
    #Return Json Format
    return _meli_refresh_token_request.content.decode('utf-8')

def meli_shipments_items(shipment_number):
    authorization = request.headers.get('Authorization')
    if authorization != (app.config['AUTHORIZATION']):
        return jsonify({'message': "unauthorized access"}), 401
    user_id = app.config['MELI_USER_ID']
    _meli_shipments = token_by_userid(user_id)
    access_token = _meli_shipments.access_token
    _meli_shipments_items_resource = "/shipments/"
    _meli_shipments_items_headers = {
        'Authorization': 'Bearer ' + access_token
    }
    _meli_shipments_items_request = requests.get(
        app.config['MELI_API_URI'] + _meli_shipments_items_resource + shipment_number + "/items", headers=_meli_shipments_items_headers)
    #Return Json Format
    _meli_shipments_items_json = json.loads(_meli_shipments_items_request.content.decode('utf-8'))
    if not "error" in _meli_shipments_items_json:
        return jsonify(_meli_shipments_items_json),200
    else:
        return jsonify({'message': "error to fecthed items"}), 500

def meli_item_id(item_id):
    user_id = app.config['MELI_USER_ID']
    _meli_shipments = token_by_userid(user_id)
    access_token = _meli_shipments.access_token
    _meli_item_resource = "/items/" + str(item_id)
    _meli_item_headers = {
        'Authorization': 'Bearer ' + access_token
    }
    _meli_item_request = requests.get(
        app.config['MELI_API_URI'] + _meli_item_resource, headers=_meli_item_headers)
    #Return Json Format
    _meli_item_json = json.loads(_meli_item_request.content.decode('utf-8'))
    if not "error" in _meli_item_json:
        return jsonify(_meli_item_json),200
    else:
        return jsonify({'message': "error to fecthed items"}), 500

def meli_order_id(order_id):
    user_id = app.config['MELI_USER_ID']
    _meli_shipments = token_by_userid(user_id)
    access_token = _meli_shipments.access_token
    _meli_order_resource = "/orders/" + str(order_id)
    _meli_order_headers = {
        'Authorization': 'Bearer ' + access_token
    }
    _meli_order_request = requests.get(
        app.config['MELI_API_URI'] + _meli_order_resource, headers=_meli_order_headers)
    #Return Json Format
    _meli_order_json = json.loads(_meli_order_request.content.decode('utf-8'))
    if not "error" in _meli_order_json:
        return jsonify(_meli_order_json),200
    else:
        return jsonify({'message': "error to fecthed items"}), 500