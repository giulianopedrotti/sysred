# -----------------------------------
#      Scheduler View
# -----------------------------------
from app import db, app
from app.views.meli import meli_refresh_token, token_by_userid
import json
from datetime import datetime, timedelta

app_id = app.config['MELI_CLIENT_ID']
secret_key = app.config['MELI_CLIENT_SECRET']
user_id = app.config['MELI_USER_ID']

"""Realiza a atualização do token"""
def refresh_token():
    meli = token_by_userid(user_id)
    refresh_token = meli.refresh_token
    meli_token = meli_refresh_token(app_id, secret_key, refresh_token)
    meli_token_json = json.loads(meli_token)
    meli.access_token = meli_token_json['access_token']
    meli.token_type = meli_token_json['token_type']
    meli.expires_in = meli_token_json['expires_in']
    meli.expires_datetime = datetime.now() + timedelta(seconds=meli_token_json['expires_in'])
    meli.scope = meli_token_json['scope']
    meli.user_id = meli_token_json['user_id']
    meli.refresh_token = meli_token_json['refresh_token']
    app.config['MELI_ACCESS_TOKEN'] = meli_token_json['access_token']
    db.session.commit()
