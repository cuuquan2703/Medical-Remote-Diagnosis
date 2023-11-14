from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class UserModel(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.String(),primary_key = True)
    salt = db.Column(db.String())
    password = db.Column(db.String())


    def __init__(self, username=None, salt=None, password=None) -> None:
        self.username = username
        self.salt = salt
        self.password = password                                

    def __repr__(self) -> str:
        return f"{self.username}:{self.password}"
