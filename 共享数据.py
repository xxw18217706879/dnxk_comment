from config import *
import pymongo

client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]
table=db[MONGO_TABLE]

results=table.find()
print(results)
