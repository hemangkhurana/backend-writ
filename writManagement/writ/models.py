from django.db import models
import pymongo
from datetime import datetime
import gridfs
from mongodb_connection import writDB

writs = writDB['writs']

# gridfs for storing pdfs
gridFSWrit =  gridfs.GridFS(writDB, collection='writ-pdfs')





















#this just contain initial and overhead idea how writs will be processed 



#### THERE IS NO PRATICAL USE OF THESE ####
# writ_temp = {
    
#     'writNumber' : None,
#     'writDate' : None,
#     'writPetitionerName' : None,
#     'writRespondentNames' : [],
#     'writPetitionerPrayer' : None,
#     'writCourtOrder' : None,
#     'writDcComments' : None,
#     'writPriority' : None,
#     'writFileAttachment' : None, # dont know
#     'writDepartment' : None,
#     'parawisedRemarks' : None,
#     'filterDateList' : [],
#     'writMaxValue' : [],
#     'counterList' : [],
#     'courtOrderList' : [],
#     'contemptCase' : None
# }

# remarks_temp = {
#     'writNumber' : None,
#     'remarkDate' : None,
#     'paraRemark' : None,
#     'setRemarkDcComments' : None,
#     'remarkFileAttachment' : None, # need to see
# }

# counters_temp = {
#     'writNumber' : None,
#     'counterDate' : None,
#     'counterText' : None,
#     'dcComments' : None,
#     'fileFttachment' : None, # need to see
# }

# court_order_temp = {
#     'writNumber' : None,
#     'orderDate' : None,
#     'orderText' : None,
#     'dcComments' : None,
#     'fileFttachment' : None, # need to see
# }

# contempt_temp = {
#     'writNumber' : None,
#     'contemptDate' : None,
#     'contemptText' : None,
#     'contemptDcComments' : None,
#     'contemptFileAttachment' : None, # need to see
# }

# data = {
#     'writ' : writ_temp,
#     'remark' : remarks_temp,
#     'counter' : counters_temp,
#     'court-order' : court_order_temp,
#     'contempt' : contempt_temp
# }