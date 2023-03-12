import os
import pymongo
import gridfs


client = pymongo.MongoClient(host=os.getenv("MONGODB_SERVICE_NAME"))
fs = gridfs.GridFS(client.gridfs_exampledb)

