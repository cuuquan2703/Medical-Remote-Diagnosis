from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class UserModel(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.String(),primary_key = True)
    salt = db.Column(db.String())
    password = db.Column(db.String())
    image_path = db.Column(db.String(), nullable=True)

    def __init__(self, username=None, salt=None, password=None, img_path=None) -> None:
        self.username = username
        self.salt = salt
        self.password = password
        self.image_path = img_path
                                        

    def __repr__(self) -> str:
        return f"{self.username}:{self.password}"
