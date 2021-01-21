import requests
import json
import sys
import os
import urllib.parse
import pandas as pd

sys.path.insert(1, './libs')
sys.path.insert(1, './responses')
sys.path.insert(1, './transformers')
import DataUtils
import WLMTransformers
import StdResponses
import StdAPIUtils


def get_workitem_delete_resources(crversion,sessionname,token,JsonData):
    Headers = StdAPIUtils.get_api_call_headers(crversion,token)

    queueID = JsonData['queueID']
    workitemID = JsonData['workitemID']

    if (crversion == "A2019.18"):

        api_op = "/v3/wlm/queues/"+queueID+"/workitems/"+workitemID
        api_call_type = "DELETE"

        return True,api_call_type,api_op,Headers,None
    else:
        return False,None,None,None,None

def get_workitem_info_resources(crversion,sessionname,token,JsonData):
    Headers = StdAPIUtils.get_api_call_headers(crversion,token)

    queueID = JsonData['queueID']
    workitemID = JsonData['workitemID']

    if (crversion == "A2019.18"):

        api_op = "/v3/wlm/queues/"+queueID+"/workitems/"+workitemID
        api_call_type = "GET"

        return True,api_call_type,api_op,Headers,None
    else:
        return False,None,None,None,None



def get_workitem_upload_resources(crversion,sessionname,token,JsonData):
    Headers = StdAPIUtils.get_api_call_headers(crversion,token)

    queueID = JsonData['queueID']
    JsonWorkItems = JsonData['JsonWorkItems']

    if (crversion == "A2019.18"):

        api_op = "/v3/wlm/queues/"+queueID+"/workitems"
        api_call_type = "POST"
        Body = JsonWorkItems

        return True,api_call_type,api_op,Headers,Body #payload.encode("utf-8")
    else:
        return False,None,None,None,None


def get_queue_structure_resources(crversion,sessionname,token,JsonData):
    queueID = JsonData['queueID']
    Headers = StdAPIUtils.get_api_call_headers(crversion,token)

    if (crversion == "A2019.18"):
        api_op = "/v3/wlm/workitemmodels/"+queueID
        api_call_type = "GET"
        return True,api_call_type,api_op,Headers,None
    else:
        return False,None,None,None,None

def get_queue_users_resources(crversion,sessionname,token,JsonData,UserType):
    queueID = JsonData['queueID']
    Headers = StdAPIUtils.get_api_call_headers(crversion,token)

    if (crversion == "A2019.18"):
        api_op = "/v3/wlm/queues/"+queueID+"/"+UserType
        api_call_type = "GET"
        return True,api_call_type,api_op,Headers,None
    else:
        return False,None,None,None,None

def get_queue_owners_resources(crversion,sessionname,token,JsonData):
    return get_queue_users_resources(crversion,sessionname,token,JsonData,"members")

def get_queue_participants_resources(crversion,sessionname,token,JsonData):
    return get_queue_users_resources(crversion,sessionname,token,JsonData,"participants")

def get_queue_consumers_resources(crversion,sessionname,token,JsonData):
    return get_queue_users_resources(crversion,sessionname,token,JsonData,"consumers")

def get_workitem_info_resources(crversion,sessionname,token,JsonData):

    queueID = JsonData['queueID']
    workitemID = JsonData['workitemID']
    Headers = StdAPIUtils.get_api_call_headers(crversion,token)

    if (crversion == "A2019.18"):
        api_op = "/v3/wlm/queues/"+queueID+"/workitems/"+workitemID
        api_call_type = "GET"
        return True,api_call_type,api_op,Headers,None
    else:
        return False,None,None,None,None


def get_queue_info_resources(crversion,sessionname,token,JsonData):

    queueID = JsonData['queueID']
    Headers = StdAPIUtils.get_api_call_headers(crversion,token)

    if (crversion == "A2019.18"):
        api_op = "/v3/wlm/queues/"+queueID
        api_call_type = "GET"
        return True,api_call_type,api_op,Headers,None
    else:
        return False,None,None,None,None

def get_workitem_list_resources(crversion,sessionname,token,JsonData):

    queueID = JsonData['queueID']
    Headers = StdAPIUtils.get_api_call_headers(crversion,token)

    if (crversion == "A2019.18"):
        api_op = "/v3/wlm/queues/"+queueID+"/workitems/list"
        api_call_type = "POST"
        Body = json.dumps(
        {
            "sort": [
                {
                    "field": "computedStatus",
                    "direction": "asc"
                }
            ],
            "filter": {},
            "fields": [],
            "page": {
                "length": 100,
                "offset": 0
            }
        }
        )
        return True,api_call_type,api_op,Headers,Body
    else:
        return False,None,None,None,None

def get_queue_list_resources(crversion,sessionname,token,JsonData):

    Headers = StdAPIUtils.get_api_call_headers(crversion,token)

    if (crversion == "A2019.18"):

        api_op = "/v3/wlm/queues/list"
        api_call_type = "POST"

        Body = json.dumps(
            {
                "sort": [
                    {
                        "field": "name",
                        "direction": "asc"
                    }
                ],
                "filter": {},
                "fields": [],
                "page": {
                    "offset": 0,
                    "total": 2,
                    "totalFilter": 2,
                    "length": 100
                }
            }
        )

        return True,api_call_type,api_op,Headers,Body
    else:
        return False,None,None,None,None

def wlm_add_workitems(outputFormat,sessionname,queueID,JsonStringOfWorkitemsToAdd):
    #{"workItems":[{"json": {"firstname": "Yli","lastname": "Z","dob": "1111111","membershipnumber": ""}}]}
    jsonData = {"queueID":queueID,"JsonWorkItems":JsonStringOfWorkitemsToAdd}
    StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_workitem_upload_resources,jsonData,WLMTransformers.GetCsvWorkitemUploadAsCsv)

def wlm_queue_list(outputFormat,sessionname):
    StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_queue_list_resources,{},WLMTransformers.GetListAsCsv)

def wlm_queue_show(outputFormat,sessionname,queueID,InfoType):
    if(InfoType.upper() == "PARTICIPANTS"):
        wlm_queue_get_participants_list(outputFormat,sessionname,queueID)
    if(InfoType.upper() == "OWNERS"):
        wlm_queue_get_owners_list(outputFormat,sessionname,queueID)
    if(InfoType.upper() == "CONSUMERS"):
        wlm_queue_get_consumers_list(outputFormat,sessionname,queueID)

def wlm_queue_workitem_list(outputFormat,sessionname,queueID):
    jsonData = {"queueID":queueID}
    StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_workitem_list_resources,jsonData,WLMTransformers.GetWorkitemListAsCsv)

def wlm_queue_get_consumers_list(outputFormat,sessionname,queueID):
    jsonData = {"queueID":queueID}
    StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_queue_consumers_resources,jsonData,WLMTransformers.GetQueueInfoAsCsv)

def wlm_queue_get_participants_list(outputFormat,sessionname,queueID):
    jsonData = {"queueID":queueID}
    StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_queue_participants_resources,jsonData,WLMTransformers.GetQueueInfoAsCsv)

def wlm_queue_get_owners_list(outputFormat,sessionname,queueID):
    jsonData = {"queueID":queueID}
    StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_queue_owners_resources,jsonData,WLMTransformers.GetQueueInfoAsCsv)

#get_workitem_info_resources
def workitem_show(outputFormat,sessionname,queueID,workitemID):
    jsonData = {"queueID":queueID,"workitemID":workitemID}
    StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_workitem_info_resources,jsonData,WLMTransformers.GetWorkitemInfoAsCsv)

def workitem_delete(outputFormat,sessionname,queueID,workitemIDs):

    ListOfWorkitemIDs = workitemIDs.lower().split(",")
    ListOfWorkitemNumIDs = [s for s in ListOfWorkitemIDs if s.isdigit()]
    ListOfWorkitemNONNumIDs = [s for s in ListOfWorkitemIDs if not s.isdigit()]
    if(len(ListOfWorkitemNONNumIDs)>0):
        print("Error: Some Workitem IDs are not Numbers: "+str(ListOfWorkitemNONNumIDs))
        exit(99)

    AllRows = []
    for workitemID in ListOfWorkitemNumIDs:

        jsonData = {"queueID":queueID,"workitemID":workitemID}

        RetCode = StdAPIUtils.generic_api_call_handler_no_post(outputFormat,sessionname,get_workitem_delete_resources,jsonData)
        if(RetCode == 204):
            aRow = {'QueueID':queueID,'WorkitemID':workitemID,'DeleteSuccess':True}
            AllRows.append(aRow)
        else:
            aRow = {'QueueID':queueID,'WorkitemID':workitemID,'DeleteSuccess':False}
            AllRows.append(aRow)

    FinalDF = pd.DataFrame(AllRows)
    if (outputFormat == "DF"):
        print(FinalDF)
    elif (outputFormat == "CSV"):
        print(FinalDF.to_csv(index=False))
    else:
        print(FinalDF.to_json())
