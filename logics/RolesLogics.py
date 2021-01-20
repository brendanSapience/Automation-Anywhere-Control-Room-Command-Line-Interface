import requests
import json
import sys
import os
import urllib.parse

sys.path.insert(1, './libs')
sys.path.insert(1, './responses')
sys.path.insert(1, './transformers')
import DataUtils
import StdResponses
import RolesTransformers
import StdAPIUtils

def get_role_list_resources(crversion,sessionname,token,JsonData):
    Headers = StdAPIUtils.get_api_call_headers(crversion,token)
    if (crversion == "A2019.18"):

        api_op = "/v1/usermanagement/roles/list"
        api_call_type = "POST"

        Body = json.dumps(
            {
                "sort":
                    [
                        {
                        "field":"name",
                        "direction":"asc"
                        }
                    ],
                "filter":{},
                "fields":[],
                "page":
                {
                "length":200,
                "offset":0
                }
            }
        )

        return True,api_call_type,api_op,Headers,Body
    else:
        return False,None,None,None,None

def role_list(outputFormat,sessionname):
    StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_role_list_resources,{},RolesTransformers.GetListAsCsv)
