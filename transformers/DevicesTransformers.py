import json
import pandas as pd

def GetListAsCsv(jsonResults):

    AllRows = []

    out_df = pd.DataFrame(columns=['id','type','hostName','userId','userName','status','poolName','fullyQualifiedHostName','updatedBy','updatedOn'])

    DeviceList = jsonResults['list']
    for device in DeviceList:
        ID = device['id']
        TYPE = device['type']
        HOST = device['hostName']
        STATUS = device['status']
        POOLNAME = device['poolName']
        UPDATEDBY = device['updatedBy']
        UPDATEDON = device['updatedOn']
        DEVICEVERSION = device['botAgentVersion']
        LIFESPAN = device['lifespan']


        new_row = {'id':ID,'type':TYPE,'hostName':HOST,'status':STATUS,'poolName':POOLNAME,'updatedBy':UPDATEDBY,'updatedOn':UPDATEDON}
        AllRows.append(new_row)

        myDFAdditional = pd.DataFrame(AllRows)

    FinalDF = pd.DataFrame(AllRows)
    return FinalDF
