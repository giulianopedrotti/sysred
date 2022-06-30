import configparser
import os
import random
import string

# Armazena a localização atual do arquivo
basedir = os.path.dirname(os.path.realpath(__file__))

# Ler as configurações do banco de um arquivo
config = configparser.ConfigParser()
config.read(f'{basedir}/config.ini')
config.read(f'{basedir}/config.ini')
user = config['DATABASE']['user']
passwd = config['DATABASE']['passwd']
database = config['DATABASE']['db']
host = config['DATABASE']['host']
port = int(config['DATABASE']['port'])
gen = string.ascii_letters + string.digits + string.ascii_uppercase
key = ''.join(random.choice(gen) for i in range(12))

# Definições do banco de dados e app
# Gera uma chave aleatória para aplicação a cada execução do servidor

SQLALCHEMY_DATABASE_URI = f'mysql://{user}:{passwd}@{host}:{port}/{database}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {
    'connect_args': {
        'connect_timeout': 10
    }
}
SECRET_KEY = key
DEBUG = True
AUTHORIZATION = config['AUTHORIZATION']['token_key']
MELI_URL = config['MELI']['meli_url']
MELI_CLIENT_ID = config['MELI']['meli_client_id']
MELI_CLIENT_SECRET = config['MELI']['meli_client_secret']
MELI_REDIRECT_URI = config['MELI']['meli_redirect_uri']
MELI_API_URI = config['MELI']['meli_api_uri']
MELI_USER_ID = config['MELI']['meli_user_id']