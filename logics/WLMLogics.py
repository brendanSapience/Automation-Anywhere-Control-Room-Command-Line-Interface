import requests
import json
import sys
import os
import urllib.parse

sys.path.insert(1, './libs')
sys.path.insert(1, './responses')
sys.path.insert(1, './transformers')
import DataUtils
import WLMTransformers
import StdResponses
import StdAPIUtils

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

def wlm_queue_list(outputFormat,sessionname):
    StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_queue_list_resources,{},WLMTransformers.GetListAsCsv)

def wlm_queue_show(outputFormat,sessionname,queueID):
    jsonData = {"queueID":queueID}
    StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_queue_info_resources,jsonData,WLMTransformers.GetQueueDefinitionAsCsv)
