from pydantic import BaseModel
import bcrypt 

class Login(BaseModel):
    username:str
    password:str

class Qr(BaseModel):
    location:str

class User(BaseModel):
    username:str
    password : str

    def hash_password(self):
        self.password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
        

    @staticmethod
    def verify_password(raw_password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(raw_password.encode('utf-8'), hashed_password)


