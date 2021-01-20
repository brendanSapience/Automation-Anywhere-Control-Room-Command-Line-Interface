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
import StdResponses
import ObjectsTransformers
import StdAPIUtils

def get_bot_update_resources(crversion,sessionname,token,JsonData):

    Headers = StdAPIUtils.get_api_call_headers(crversion,token)
    ObjID = JsonData['ObjID']
    UpdatedObjectDefAsJson = JsonData['UpdatedObjectDefAsJson']

    if (crversion == "A2019.18"):

        api_op = "/v2/repository/files/"+ObjID+"/content?hasErrors=false"
        api_call_type = "PUT"

        payload = None
        with open(UpdatedObjectDefAsJson, 'r') as file:
            data = file.read() #.replace('\n', '').replace('\'','"')
            payload = data #json.loads(data)

        return True,api_call_type,api_op,Headers,payload
    else:
        return False,None,None,None,None



def get_bot_list_resources(crversion,sessionname,token,JsonData):

    objNameFilter = JsonData['objNameFilter']
    Headers = StdAPIUtils.get_api_call_headers(crversion,token)

    if (crversion == "A2019.18"):

        api_op = "/v2/repository/workspaces/private/files/list"
        api_call_type = "POST"
        f = json.loads(getFilterOnName(objNameFilter))
        Body = json.dumps(
            {
                "fields": [],
                "filter": f,
                "sort": [
                    {
                        "field": "directory",
                        "direction": "desc"
                    },
                    {
                        "field": "name",
                        "direction": "asc"
                    }
                ],
                "page": {
                    "offset": 0,
                    "length": 100
                }
            }
        )

        return True,api_call_type,api_op,Headers,Body
    else:
        return False,None,None,None,None

def get_bot_show_resources(crversion,sessionname,token,JsonData):
    ObjID = JsonData['ObjID']
    Headers = StdAPIUtils.get_api_call_headers(crversion,token)
    if (crversion == "A2019.18"):

        api_op = "/v2/repository/files/"+ObjID+"/content"
        api_call_type = "GET"

        return True,api_call_type,api_op,Headers,None
    else:
        return False,None,None,None,None


def bot_show(outputFormat,sessionname,ObjID):
    jsonData = {"ObjID":ObjID}
    json_object = StdAPIUtils.generic_api_call_handler_no_post(outputFormat,sessionname,get_bot_show_resources,jsonData)
    json_formatted_str = json.dumps(json_object, indent=2)
    return json_formatted_str

def bot_list(outputFormat,sessionname,objNameFilter):
    jsonData = {"objNameFilter":objNameFilter}
    StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_bot_list_resources,jsonData,ObjectsTransformers.GetListAsCsv)


def bot_update(outputFormat,sessionname,ObjID,UpdatedObjectDefAsJson):
    jsonData = {"UpdatedObjectDefAsJson":UpdatedObjectDefAsJson,"ObjID":ObjID}
    json_object = StdAPIUtils.generic_api_call_handler_no_post(outputFormat,sessionname,get_bot_update_resources,jsonData)
    if (outputFormat == "DF"):
        aDF = pd.DataFrame(json_object, index=[0])
        print(aDF)

    elif (outputFormat == "CSV"):
        aDF = pd.DataFrame(json_object, index=[0])
        print(aDF.to_csv(index=False))

    else:
        json_formatted_str = json.dumps(json_object, indent=2)
        print(json_formatted_str)

def getFilterOnName(ObjectName):
    jsonFilter = '{"operator":"substring","value":"'+ObjectName+'","field":"name"}'
    return jsonFilter
