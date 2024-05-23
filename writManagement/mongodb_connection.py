import pymongo

# credentials for mongngodb connection
myclient = pymongo.MongoClient("add your connection string here")

writDB = myclient["dss-writ"]
scheduleDB = myclient["dss-schedule"]
