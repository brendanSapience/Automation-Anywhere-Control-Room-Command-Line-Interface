import requests
import json
import sys
import os
import urllib.parse
sys.path.insert(1, './responses')
sys.path.insert(1, './transformers')
import DataUtils
import IQBotLITransformers
import StdResponses
import StdAPIUtils

def get_li_list_resources(crversion,sessionname,token):

    Headers = StdAPIUtils.get_api_call_headers(crversion,token)

    if (crversion == "A2019.18"):

        api_op = "/IQBot/api/projects"
        api_call_type = "GET"

        return True,api_call_type,api_op,Headers,None
    else:
        return False,None,None,None,None

def get_grp_list_from_li_resources(crversion,sessionname,token,JsonData):

    Headers = StdAPIUtils.get_api_call_headers(crversion,token)
    LiId = JsonData['LiId']
    UpdateJsonFile = JsonData['UpdatedObjectDefAsJson']

    if (crversion == "A2019.18"):

        api_op = "/IQBot/api/projects/"+LiId+"/categories?offset=0&limit=5000&sort=-index&trainingNotRequired=true"
        api_call_type = "GET"

        return True,api_call_type,api_op,Headers,None
    else:
        return False,None,None,None,None

def ConvertLINameToLIID(sessionname,liname):

    try:
        res = list_learning_instances(sessionname,False,False)
        #print(res.text)
        JsonList = json.loads(res.text)
        #print(res)
        ItemList = JsonList['data']
        #print(ItemList)
        for item in ItemList:
            ID = item['id']
            NAME = item['name']
            if(liname == NAME):
                #print(ID)
                return ID

        return ""
    except:
        print("An error occured while converting the LI Name to LI ID.")
        exit(1)

def GetAllGroupsFromLI(sessionname,liid):
    Mappings = {}
    try:

        JsonList = list_groups_from_li_internal(sessionname,liid)

        ItemList = JsonList['data']['categories']

        for item in ItemList:

            ID = item['id']
            NAME = item['name']
            GRPID = item['visionBot']['id']
            Mappings[ID] = GRPID

        return liid,Mappings
    except Exception as e:
        print("An error occured while converting getting Group List for LI:"+str(e))
        exit(1)

def list_groups_from_li_internal(sessionname,LiId):
    JsonData = {"LiId":LiId}
    json_object = StdAPIUtils.generic_api_call_handler_no_post(outputFormat,sessionname,get_grp_list_from_li_resources,JsonData)
    return json_object

def list_groups_from_li(outputFormat,sessionname,LiId):
    JsonData = {"LiId":LiId}
    StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_grp_list_from_li_resources,JsonData,IQBotLITransformers.GetListAsCsv)

def list_learning_instances(outputFormat,sessionname):
    StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_li_list_resources,{},IQBotLITransformers.GetLIListAsCsv)
