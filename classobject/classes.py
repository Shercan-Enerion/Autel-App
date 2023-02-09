from passlib.context import CryptContext
from requests import post, get
from config.bd import dataBase


class Signup:
    def __init__(self):
        self.url = 'http://141.147.133.37'
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def postUser(self, username: str, password: str, email: str):
        insert = dataBase.sendUser(
            {'email': email, 'password': password, 'username': username})
        return insert

    def getUser(self, email: str):
        get(self.url, json={'email': 'email'})


signupClass = Signup()


class Hash:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return signupClass.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return signupClass.pwd_context.hash(password)
