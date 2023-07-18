from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_migrate import Migrate

# Load environment variables from .env file
load_dotenv()

# DATABASE_URI = os.getenv('TIMESCALE_DATABASE_URI')
db_host = os.environ.get('DB_HOST', 'db')
db_port = os.environ.get('DB_PORT', '5432')
db_username = os.environ.get('DB_USERNAME', 'postgres')
db_password = os.environ.get('DB_PASSWORD')
# contants
app = Flask(__name__)
# r = redis.Redis(host='localhost', port=6379)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/postgres"
db.init_app(app)
migrate = Migrate(app, db)
