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

def get_bot_update_resources(crversion,sessionname,token,ObjID,UpdatedObjectDefAsJson):

    if (crversion == "A2019.18"):
        Headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'X-Authorization': token
        }


        api_op = "/v2/repository/files/"+ObjID+"/content?hasErrors=false"
        api_call_type = "PUT"

        payload = None
        with open(UpdatedObjectDefAsJson, 'r') as file:
            data = file.read() #.replace('\n', '').replace('\'','"')
            payload = data #json.loads(data)

        return True,api_call_type,api_op,Headers,payload
    else:
        return False,None,None,None,None



def get_bot_list_resources(crversion,sessionname,token,objNameFilter):

    if (crversion == "A2019.18"):
        Headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'X-Authorization': token
        }


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


def get_bot_show_resources(crversion,sessionname,token,ObjID):

    if (crversion == "A2019.18"):
        Headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'X-Authorization': token
        }

        api_op = "/v2/repository/files/"+ObjID+"/content"
        api_call_type = "GET"

        return True,api_call_type,api_op,Headers,None
    else:
        return False,None,None,None,None


def bot_show(outputFormat,sessionname,ObjID):

    url = DataUtils.GetUrl(sessionname)
    TOKEN = DataUtils.GetAuthToken(sessionname)
    CRVERSION = DataUtils.GetCRVersion(sessionname)

    IsVersionSupported,CallType,ApiUri,Headers,Body = get_bot_show_resources(CRVERSION,sessionname,TOKEN,ObjID)

    if not IsVersionSupported:
        logging.debug("Unsupported CR Version: {}".format(crversion))
        print("Unsupported CR Version")
        exit(1)

    FULLURL = urllib.parse.urljoin(url,ApiUri)

    response = requests.request(method=CallType, url=FULLURL, data=Body, headers=Headers)

    isAPICallOK = StdResponses.processAPIResponse(response)
    if(not isAPICallOK):
        exit(99)
    else:
        json_object = json.loads(response.text)
        json_formatted_str = json.dumps(json_object, indent=2)
        return json_formatted_str


def bot_list(outputFormat,sessionname,objNameFilter):

    url = DataUtils.GetUrl(sessionname)
    TOKEN = DataUtils.GetAuthToken(sessionname)
    CRVERSION = DataUtils.GetCRVersion(sessionname)

    IsVersionSupported,CallType,ApiUri,Headers,Body = get_bot_list_resources(CRVERSION,sessionname,TOKEN,objNameFilter)

    if not IsVersionSupported:
        logging.debug("Unsupported CR Version: {}".format(crversion))
        print("Unsupported CR Version")
        exit(1)

    FULLURL = urllib.parse.urljoin(url,ApiUri)

    response = requests.request(method=CallType, url=FULLURL, data=Body, headers=Headers)

    isAPICallOK = StdResponses.processAPIResponse(response)
    if(not isAPICallOK):
        exit(99)
    else:
        json_object = json.loads(response.text)
        if (outputFormat == "DF"):
            #print(json_object)
            aDF = ObjectsTransformers.GetListAsCsv(json_object)
            print(aDF)
        elif (outputFormat == "CSV"):
            #print(json_object)
            aDF = ObjectsTransformers.GetListAsCsv(json_object)
            print(aDF.to_csv(index=False))
        else:
            #print(json_object)
            json_formatted_str = json.dumps(json_object, indent=2)
            print(json_formatted_str)


def bot_update(outputFormat,sessionname,UpdatedObjectDefAsJson,ObjID):

    url = DataUtils.GetUrl(sessionname)
    TOKEN = DataUtils.GetAuthToken(sessionname)
    CRVERSION = DataUtils.GetCRVersion(sessionname)

    IsVersionSupported,CallType,ApiUri,Headers,Body = get_bot_update_resources(CRVERSION,sessionname,TOKEN,UpdatedObjectDefAsJson,ObjID)

    if not IsVersionSupported:
        logging.debug("Unsupported CR Version: {}".format(crversion))
        print("Unsupported CR Version")
        exit(1)

    FULLURL = urllib.parse.urljoin(url,ApiUri)

    response = requests.request(method=CallType, url=FULLURL, data=Body, headers=Headers)

    isAPICallOK = StdResponses.processAPIResponse(response)
    if(not isAPICallOK):
        exit(99)
    else:
        json_object = json.loads(response.text)
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
