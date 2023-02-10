import pymongo
import gridfs


client = pymongo.MongoClient()
fs = gridfs.GridFS(client.gridfs_exampledb)

