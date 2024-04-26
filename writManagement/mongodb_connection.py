import pymongo

# credentials for mongngodb connection
myclient = pymongo.MongoClient("mongodb+srv://dss:P8NKXqiTp3tN3vNt@dss-search.ujjrk5w.mongodb.net/?retryWrites=true&w=majority")

writDB = myclient["dss-writ"]
scheduleDB = myclient["dss-schedule"]
