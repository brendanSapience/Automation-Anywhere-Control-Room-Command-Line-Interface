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
import AdminSettingsTransformers
import StdResponses
import StdAPIUtils

def update_pwd_settings_resources(crversion,sessionname,token,JsonData):

    Headers = StdAPIUtils.get_api_call_headers(crversion,token)
    UpdatedObjectDefAsJson = JsonData['UpdatedJsonFileDef']

    if (crversion == "A2019.18"):

        api_op = "/v1/settings/password"
        api_call_type = "POST"

        payload = None
        with open(UpdatedObjectDefAsJson, 'r') as file:
            data = file.read() #.replace('\n', '').replace('\'','"')
            payload = data #json.loads(data)

        return True,api_call_type,api_op,Headers,payload
    else:
        return False,None,None,None,None



def get_admin_pwd_settings_show_resources(crversion,sessionname,token,JsonData):
    Headers = StdAPIUtils.get_api_call_headers(crversion,token)

    if (crversion == "A2019.18"):

        api_op = "/v1/settings/password"
        api_call_type = "GET"

        return True,api_call_type,api_op,Headers,None
    else:
        return False,None,None,None,None

def show_pwd_settings(outputFormat,sessionname):
    json_object = StdAPIUtils.generic_api_call_handler_no_post(outputFormat,sessionname,get_admin_pwd_settings_show_resources,{})
    json_formatted_str = json.dumps(json_object, indent=2)
    print(json_formatted_str)


def update_pwd_settings(outputFormat,sessionname,UpdatedObjectDefAsJson):
    jsonData = {"UpdatedJsonFileDef":UpdatedObjectDefAsJson}
    rep_text = StdAPIUtils.generic_api_call_handler_no_post(outputFormat,sessionname,update_pwd_settings_resources,jsonData)

    aRow = {'Status':"Error"}
    if(rep_text == "OK"):
        aRow = {'Status':"Success"}

    if (outputFormat == "DF"):
        aDF = pd.DataFrame(aRow, index=[0])
        print(aDF)

    elif (outputFormat == "CSV"):
        aDF = pd.DataFrame(aRow, index=[0])
        print(aDF.to_csv(index=False))

    else:
        json_formatted_str = json.dumps(aRow, indent=2)
        print(json_formatted_str)
