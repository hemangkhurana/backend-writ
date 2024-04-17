import pymongo
import gridfs

# credentials for mongngodb conncetion
myclient = pymongo.MongoClient("mongodb+srv://dss:P8NKXqiTp3tN3vNt@dss-search.ujjrk5w.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["dss-writ"]
writs = mydb['writs']

# gridfs for storing pdfs
gridFSWrit =  gridfs.GridFS(mydb, collection='writ-pdfs')