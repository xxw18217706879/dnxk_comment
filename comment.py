import pynlpir
import pymongo
import json
from config import *

client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]
table=db[MONGO_TABLE]

#text=db.collection_names()
results=table.find()

for result in results:
    comment=result['content']
    with open("comments.txt","a",encoding="utf8")as f:
        f.write(comment)
    print(result)
    f.close()






