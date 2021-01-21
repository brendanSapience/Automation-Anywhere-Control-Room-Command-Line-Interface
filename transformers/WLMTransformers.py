import json
import pandas as pd
from pandas.io.json import json_normalize

def GetCsvWorkitemUploadAsCsv(jsonResults):

    myDF = pd.DataFrame(jsonResults['list'])
    myDF.pop('json')
    myDF.pop('version')
    myDF.pop('result')
    myDF.pop('updatedBy')
    myDF.pop('updatedOn')
    myDF.pop('deviceUserId')
    return myDF

def GetQueueInfoAsCsv(jsonResults):
    if('roles' in jsonResults):
        jsonResults = jsonResults['roles']
    myDF = pd.DataFrame(jsonResults)
    return myDF

def GetWorkitemInfoAsCsv(jsonResults):
    myDF = json_normalize(jsonResults)
    return myDF

def GetWorkitemListAsCsv(jsonResults):

    myDF = pd.DataFrame(jsonResults['list'])
    return myDF

def GetListAsCsv(jsonResults):

    AllRows = []

    out_df = pd.DataFrame()

    ItemList = jsonResults['list']
    for item in ItemList:

        a1 = item['id']
        a2 = item['createdBy']
        a3 = item['createdOn']
        a4 = item['updatedOn']
        a5 = item['version']
        a6 = item['name']
        a7 = item['description']
        a8 = item['reactivationThreshold']
        a9 = item['status']

        b1 = item['manualProcessingTime']
        b2 = item['manualProcessingTimeUnit']
        b3 = item['workItemProcessingOrders']
        b4 = item['workItemModelId']
        b5 = item['considerReactivationThreshold']


        new_row = {'id':a1,'createdBy':a2,'createdOn':a3,
        'version':a5,'name':a6,'status':a9}

        #new_row = {'deviceName':a1,'automationName':a2,'jobName':a3,'jobFilePath':a4,'jobType':a5,'currentBotName':a6,
        #'startDateTime':a7,'endDateTime':a8,'command':a9,'jobExecutionStatus':b1,'progress':b2,'scheduleId':b3,'userId':b4,'deviceId':b5,'id':b6,
        #'currentLine':b7,'totalLines':b8,'jobId':b9,'tenantId':c1,'modifiedBy':c2,'createdBy':c3,'modifiedOn':c4,'deploymentId':c5,
        #'queueName':c6,'queueId':c7,'rdpEnabled':c8,'message':c9,'canManage':d1,'jobExecutionDetails':d2,'username':d3,'source':d4}
        AllRows.append(new_row)

    FinalDF = pd.DataFrame(AllRows)
    return FinalDF

def GetQueueDefinitionAsCsv(jsonResults):

    AllRows = []

    out_df = pd.DataFrame()

    a1 = jsonResults['id']
    a2 = jsonResults['createdBy']
    a3 = jsonResults['createdOn']
    a4 = jsonResults['updatedOn']
    a5 = jsonResults['version']
    a6 = jsonResults['name']
    a7 = jsonResults['description']
    a8 = jsonResults['reactivationThreshold']
    a9 = jsonResults['status']

    b1 = jsonResults['manualProcessingTime']
    b2 = jsonResults['manualProcessingTimeUnit']
    b3 = jsonResults['workItemProcessingOrders']
    b4 = jsonResults['workItemModelId']
    b5 = jsonResults['considerReactivationThreshold']


    new_row = {'id':a1,'createdBy':a2,'createdOn':a3,'version':a5,'name':a6,'status':a9}

    AllRows.append(new_row)

    FinalDF = pd.DataFrame(AllRows)
    return FinalDF
