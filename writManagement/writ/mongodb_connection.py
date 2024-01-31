import pymongo
import gridfs

myclient = pymongo.MongoClient("mongodb+srv://dss:P8NKXqiTp3tN3vNt@dss-search.ujjrk5w.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["dss-writ"]
writs = mydb['writs']

gridFSWrit =  gridfs.GridFS(mydb, collection='writ-pdfs')