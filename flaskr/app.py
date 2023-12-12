from flask import Flask
from .routes import  abp
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models.user_model import db
from flask_cors import CORS, cross_origin
from .config import *

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SQLALCHEMY_DATABASE_URI'] =  f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost:{DB_PORT}/{DB_TABLE}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app,db)

app.register_blueprint(abp)
# app.register_blueprint(ibp)

if __name__ == "__main__":
    app.run()

