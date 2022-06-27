import datetime
from app import db, ma

"""Definição da classe/tabela dos usuários e seus campos"""
class Meli(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meli_code = db.Column(db.String(45), unique=True, nullable=False)
    access_token = db.Column(db.String(100), nullable=False)
    token_type = db.Column(db.String(45), nullable=False)
    expires_in = db.Column(db.Integer, nullable=False)
    expires_datetime = db.Column(db.DateTime, nullable=False)
    scope = db.Column(db.String(45), unique=True, nullable=False)
    user_id = db.Column(db.String(45), unique=True, nullable=False)
    refresh_token = db.Column(db.String(45), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, meli_code, access_token, token_type, expires_in, expires_datetime, scope, user_id, refresh_token):
        self.meli_code = meli_code
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.expires_datetime = expires_datetime
        self.scope = scope
        self.user_id = user_id
        self.refresh_token = refresh_token


"""Definindo o Schema do Marshmallow para facilitar a utilização de JSON"""
class MeliSchema(ma.Schema):
    class Meta:
        fields = ('id', 'meli_code', 'access_token', 'token_type', 'expires_in', 'expires_datetime', 'scope', 'user_id', 'refresh_token', 'created_on')


meli_schema = MeliSchema()
melis_schema = MeliSchema(many=True)