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
    elif "not_found_shipping_id" in _meli_shipments_items_json:
        return jsonify({'error': "not_found_shipping_id"}), 404
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
    elif "order_not_found" in _meli_order_json:
        return jsonify({'error': "order_not_found"}), 404
    else:
        return jsonify({'message': "error to fecthed items"}), 500

def meli_inova_id(order_ship_id,fil=''):
    authorization = request.headers.get('Authorization')
    if authorization != (app.config['AUTHORIZATION']):
        return jsonify({'message': "unauthorized access"}), 401
    user_id = app.config['MELI_USER_ID']
    meli_db_info = token_by_userid(user_id)
    meli_access_token = meli_db_info.access_token
    meli_inova_headers = {
        'Authorization': 'Bearer ' + meli_access_token
    }
    def meli_inova(path,id):
        meli_inova_resource = path + str(id)
        meli_inova_request = requests.get(
            app.config['MELI_API_URI'] + meli_inova_resource, headers=meli_inova_headers)
        #Return Json Format
        return json.loads(meli_inova_request.content.decode('utf-8'))
    meli_inova_ship_details = meli_inova("/shipments/",order_ship_id)
    meli_inova_order_json = []
    meli_inova_ship_json = []
    meli_inova_items_json = []
    if "error" in meli_inova_ship_details:
        if "not_found_shipping_id" == meli_inova_ship_details['error']:
            meli_inova_order_details = meli_inova("/orders/",order_ship_id)
            meli_inova_ship_details = meli_inova("/shipments/",meli_inova_order_details['shipping']['id'])
    else:
        meli_inova_order_details = meli_inova("/orders/",meli_inova_ship_details['order_id'])
    meli_inova_nfe_details = meli_inova("/users/",str(meli_inova_order_details['buyer']['id']) + "/invoices/shipments/" + str(meli_inova_order_details['shipping']['id']))
    meli_inova_item_details = meli_inova("/items/",str(meli_inova_order_details['order_items'][0]['item']['id']))
    meli_inova_order_json.append({
            "user_id": meli_inova_order_details['buyer']['id'],
            "first_name": meli_inova_order_details['buyer']['first_name'],
            "last_name": meli_inova_order_details['buyer']['last_name'],
            "nickname": meli_inova_order_details['buyer']['nickname'],
            "cpf": meli_inova_nfe_details['recipient']['identifications']['cpf'],
            "phone": meli_inova_nfe_details['recipient']['phone']['area_code'] + meli_inova_nfe_details['recipient']['phone']['number'],
            "address_line": meli_inova_ship_details['receiver_address']['address_line'],
            "city": meli_inova_ship_details['receiver_address']['city']['name'],
            "state": meli_inova_ship_details['receiver_address']['state']['name'],
            "zip_code": meli_inova_ship_details['receiver_address']['zip_code'],
            "secure_thumbnail": meli_inova_item_details['secure_thumbnail']
        })
    for key in meli_inova_order_details['order_items']:
            print(key['item']['seller_sku'])
            meli_inova_items_json.append({
                "item_id": key['item']['id'],
                "seller_sku": key['item']['seller_sku'],
                "title": key['item']['title'],
                "quantity": key['quantity'],
                "sale_fee": key['sale_fee'],
                "unit_price": key['unit_price']
                })
    
    
    if (fil == ''):
        if not "error" in meli_inova_order_json:
            meli_inova_order_json.append(meli_inova_items_json)
            return jsonify(meli_inova_order_json),200
        else:
            return jsonify({'message': "error to fecthed inova items"}), 500
    if (fil == 'items'):
        if not "error" in meli_inova_items_json:
            return jsonify(meli_inova_items_json),200
        else:
            return jsonify({'message': "error to fecthed inova items"}), 500
    if (fil == 'info'):
        if not "error" in meli_inova_order_json:
            return jsonify(meli_inova_order_json),200
        else:
            return jsonify({'message': "error to fecthed inova items"}), 500


    
    