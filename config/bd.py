from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.errors import ExecutionTimeout
from os import getenv
load_dotenv()


class BaseData():
    def __init__(self):
        self.conn = MongoClient(
            "mongodb+srv://yess:"+getenv('ACCESS_TOKEN')+"@cluster0.wdzh1o3.mongodb.net/?retryWrites=true&w=majority")[getenv('DATABASE')]
        self.__dictGet = {}
        self.__conn = MongoClient(
            "mongodb+srv://yess:"+getenv('ACCESS_TOKEN')+"@cluster0.wdzh1o3.mongodb.net/?retryWrites=true&w=majority")[getenv('DATABASE')]
        self.data = {}

    def sendData(self, data):
        self.data = data
        # self.__conn['Variables'].insert_one(self.data)

    def readData(self, *args, limite: int = 100):
        '''
        parameters:
        limit: limit of data
        type_limit: int
        ([{'client': 'CLI-IA-DM-23'}, {'30': 1}],)'''
        if len(args) > 0:
            return self.__conn['Variables'].find(args[0][0], args[0][1]).limit(limite)
        else:
            return self.__conn['Variables'].find().limit(limite)

    def sendUser(self, data):
        insert = {
            '_id': data['email'], 'username': data['username'], 'password': data['password']}
        try:
            insertOut = self.__conn['Users'].insert_one(insert)
            return str(insertOut.inserted_id)
        except:
            return None

    def sendClient(self, data):
        data['_id'] = data['client']
        data.pop('client')
        self.__conn['Clients'].insert_one(data)

    def readUser(self, **kwargs):
        if len(kwargs) > 0:
            for key, value in kwargs.items():
                if key == 'id':
                    key = '_id'
                self.__dictGet[key] = value
            try:
                returned = self.__conn['Users'].find(
                    self.__dictGet, max_time_ms=5000)
            except ExecutionTimeout:
                return None
        else:
            try:
                returned = self.__conn['Users'].find(max_time_ms=5000)
            except ExecutionTimeout:
                returned = None
        return returned

    def readDataData(self):
        try:
            returned = self.__conn['Data'].find(max_time_ms=5000)
        except ExecutionTimeout:
            returned = None
        return returned


dataBase = BaseData()
