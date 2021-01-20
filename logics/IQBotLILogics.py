import requests
import json
import sys
import os
import urllib.parse

sys.path.insert(1, './libs')
sys.path.insert(1, './responses')
sys.path.insert(1, './transformers')
import DataUtils
import IQBotLITransformers
import IQBotCommons
import StdResponses
import StdAPIUtils

def get_li_file_list_per_status_resources(crversion,sessionname,token,JsonData):
    ValidStatuses = ['VALIDATION', 'INVALID', 'SUCCESS', 'UNCLASSIFIED', 'UNTRAINED']

    Headers = StdAPIUtils.get_api_call_headers(crversion,token)
    Status = JsonData['Status']
    LiId = JsonData['LiId']

    if (crversion == "A2019.18"):

        if Status.upper() not in ValidStatuses:
            print("Error: Invalid File Status: "+STATUS)
            exit(1)

        api_op = "/IQBot/gateway/learning-instances/"+LiId+"/files/list?docStatus="+Status.upper()
        api_call_type = "GET"

        return True,api_call_type,api_op,Headers,None
    else:
        return False,None,None,None,None

def get_li_detail_resources(crversion,sessionname,token,LiId):

    if (crversion == "A2019.18"):
        Headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'x-authorization': token
        }

        api_op = "/IQBot/api/projects/"+LiId+"/detail-summary"
        api_call_type = "GET"

        return True,api_call_type,api_op,Headers,None
    else:
        return False,None,None,None,None

def get_li_file_list_resources(crversion,sessionname,token,LiId):

    if (crversion == "A2019.18"):
        Headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'X-Authorization': token
        }

        api_op = "/IQBot/api/projects/"+LiId+"/files"
        api_call_type = "GET"

        return True,api_call_type,api_op,Headers,None
    else:
        return False,None,None,None,None

def get_li_grp_list_resources(crversion,sessionname,token,JsonData):

    Headers = StdAPIUtils.get_api_call_headers(crversion,token)
    LiId = JsonData['LiId']

    if (crversion == "A2019.18"):

        api_op = "/IQBot/api/projects/"+LiId+"/categories?offset=0&limit=50&sort=-index&trainingNotRequired=true"
        api_call_type = "GET"

        return True,api_call_type,api_op,Headers,None
    else:
        return False,None,None,None,None

def get_learning_instance_detail(outputFormat,sessionname,LiId):
    JsonData = {"LiId":LiId}
    StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_li_detail_resources,JsonData,IQBotLITransformers.GetListAsCsv)


def list_learning_instance_files(outputFormat,sessionname,LiId, Status):
    if(Status == ""):
        JsonData = {"LiId":LiId}
        StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_li_file_list_resources,JsonData,IQBotLITransformers.GetLIFileListAsCsv)

    else:
        JsonData = {"LiId":LiId,"Status":Status}
        StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_li_file_list_per_status_resources,JsonData,IQBotLITransformers.GetFileListPerStatusAsCsv)


def list_learning_instance_groups(outputFormat,sessionname,LiId):
    JsonData = {"LiId":LiId}
    StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_li_grp_list_resources,JsonData,IQBotLITransformers.GetLIGroupListAsCsv)
