#db.py
from pymongo import MongoClient
import certifi
ca = certifi.where()

# MongoDB Connection
db_name = "ProjectDB"
uri = "mongodb+srv://username:password@projectdb.hqhfhil.mongodb.net/" #Username password girip veri tabanı bağlantısına bağla
client = MongoClient(uri,tlsCAFile=ca)
db = client["ProjectDB"]
user_col = db["Users"]
qr_col = db["Qr"]

collection = db.test_collection
