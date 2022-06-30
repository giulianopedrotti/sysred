from flask import Flask, jsonify, Blueprint
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import os, socket

# Start Flask Framework
app = Flask(__name__)
# Load configuration from file config.py
app.config.from_object('config')
# Secret Key for use session
app.secret_key = os.urandom(12)
# Change path static
static_path = Blueprint('app', __name__, static_folder='static/',static_url_path='/login/static/')
app.register_blueprint(static_path)

db = SQLAlchemy(app)
ma = Marshmallow(app)

print(app.config['MELI_CLIENT_ID'])

from .models import users
from .models import meli
from .models import scheduler
from .routes import routes
from .views import users
from .views import meli
from .views import scheduler

