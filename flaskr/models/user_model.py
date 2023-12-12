from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()
class UserModel(db.Model):

    __tablename__ = 'users'

    id  = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    salt = db.Column(db.String())
    password = db.Column(db.String())
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())


    def __init__(self, username=None, salt=None, password=None) -> None:
        self.username = username
        self.salt = salt
        self.password = password                                

    def __repr__(self) -> str:
        return f"{self.username}:{self.password}"
