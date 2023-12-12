from datetime import datetime
from sqlalchemy import Sequence
from .user_model import db
#db = SQLAlchemy()
class ImageModel(db.Model):
    
    __tablename__ = 'Upload_image'
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(), nullable=False, primary_key=True)
    path = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    result = db.Column(db.String(255))

    def __init__(self, username=None, path=None, result=None) -> None:
        self.username = username
        self.path = path
        self.result ="result"

    def __repr__(self) -> str:
        return f"{self.username}:{self.path}"