from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_migrate import Migrate

# Load environment variables from .env file
load_dotenv()

# DATABASE_URI = os.getenv('TIMESCALE_DATABASE_URI')
# contants
app = Flask(__name__)
# r = redis.Redis(host='localhost', port=6379)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:example@localhost:5432/postgres'
db.init_app(app)
migrate = Migrate(app, db)
