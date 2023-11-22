from ..models.user_model import UserModel
import hashlib
from ..config import STATIC, HASHING_METHOD
from werkzeug.security import generate_password_hash,check_password_hash

class AuthService():
    def __init__(self,auth_model) -> None:
        self.auth_model = auth_model
        pass

    def check_password(self,password,salt,password_in_db,method = HASHING_METHOD):
        print(HASHING_METHOD)
        hash_password = "$".join([method,salt,password_in_db])

        check = password
        print(hash_password)
        if check_password_hash(hash_password,check):
            return True
        else:
            return False
        
    def find_user(self, username):
        exist_user = self.auth_model.query.filter_by(username=username).all()
        return exist_user
    
    def create_new_user(self,username,password):
        hash_password = generate_password_hash(password,method=HASHING_METHOD).split("$")
        algo = hash_password[0]
        _salt = hash_password[1]
        new_password = hash_password[2]
        return self.auth_model(username=username, salt=_salt,password=new_password)

    def create_hashing_password(self,password, method=HASHING_METHOD):
        hash_password = generate_password_hash(password,method)
        hash_password = hash_password.split("$")
        algo = hash_password[0]
        salt = hash_password[1]
        new_password = hash_password[2]
        return{
            'full_hash_password': hash_password,
            'part': (new_password,salt,algo)
        }