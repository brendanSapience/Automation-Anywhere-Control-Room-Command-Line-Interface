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
import CredentialsTransformers
import StdResponses
import StdAPIUtils

def get_queue_list_resources(crversion,sessionname,token,JsonData):

    Headers = StdAPIUtils.get_api_call_headers(crversion,token)

    if (crversion == "A2019.18"):

        api_op = "/v1/credentialvault/credentials/list"
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
                    "length": 100,
                    "offset": 0
                }
            }
        )

        return True,api_call_type,api_op,Headers,Body
    else:
        return False,None,None,None,None


def get_queue_show_resources(crversion,sessionname,token,JsonData):
    CredsID = JsonData['credsID']
    Headers = StdAPIUtils.get_api_call_headers(crversion,token)

    if (crversion == "A2019.18"):

        api_op = "/v1/credentialvault/credentials/"+CredsID
        api_call_type = "GET"

        return True,api_call_type,api_op,Headers,None
    else:
        return False,None,None,None,None

def credentials_list(outputFormat,sessionname):
    #{"workItems":[{"json": {"firstname": "Yli","lastname": "Z","dob": "1111111","membershipnumber": ""}}]}
    StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_queue_list_resources,{},CredentialsTransformers.GetCsvCredsList)

def credentials_show(outputFormat,sessionname,CredsID):
    jsonData = {"credsID":CredsID}
    StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_queue_show_resources,jsonData,CredentialsTransformers.GetCsvCredsShow)
