import requests
import json
import sys
import os
import urllib.parse
import pandas as pd

sys.path.insert(1, './libs')
sys.path.insert(1, './transformers')

import DataUtils
import IQBotGroupTransformers
import IQBotCommons
import StdResponses
import StdAPIUtils

def get_group_list_resources(crversion,sessionname,token):
    Headers = StdAPIUtils.get_api_call_headers(crversion,token)
    if (crversion == "A2019.18"):
        api_op = "/IQBot/api/bots"
        api_call_type = "GET"
        return True,api_call_type,api_op,Headers,None
    else:
        return False,None,None,None,None

def get_group_update_resources(crversion,sessionname,token,JsonData):
    Headers = StdAPIUtils.get_api_call_headers(crversion,token)
    GrpId = JsonData['GrpId']
    GroupName = JsonData['GroupName']
    LiID = JsonData['LiId']
    NewStatus = JsonData['NewStatus']

    VALIDACTIONS = ['ON','OFF']
    if (crversion == "A2019.18"):
        #print("STATUS:"+NewStatus)
        NewState = ""
        Body = ""
        if(NewStatus.upper() in VALIDACTIONS):
            if(NewStatus.upper() == VALIDACTIONS[0]):
                NewState = 'production'
            if(NewStatus.upper() == VALIDACTIONS[1]):
                NewState = 'staging'

        Body = json.dumps(
            {
            "state": NewState.lower()
            }
        )

        api_op = "/IQBot/api/projects/"+LiID+"/categories/"+GroupNumber+"/bots/"+GroupID+"/state"
        api_call_type = "POST"
        return True,api_call_type,api_op,Headers,Body
    else:
        return False,None,None,None,None

def list_groups(outputFormat,sessionname):
    StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_group_list_resources,{},IQBotGroupTransformers.GetGroupListAsCsv)

def change_group_status(outputFormat,sessionname,LiID,GroupNum,NewStatus):

    url = DataUtils.GetUrl(sessionname)
    TOKEN = DataUtils.GetAuthToken(sessionname)
    CRVERSION = DataUtils.GetCRVersion(sessionname)

    liid,groupMappings = IQBotCommons.GetAllGroupsFromLI(sessionname,LiID)

    AllGroups = []
    if("," in GroupNum):
        AllGroups = GroupNum.split(",")
    elif(GroupNum.upper() in ["ALL","ALLGROUPS","ALLGRPS","EVERYTHING"]):
        AllGroups = list(groupMappings.keys())
    else:
        AllGroups.append(GroupNum)

    AllRows = []
    for Grp in AllGroups:
        GrpId = groupMappings[Grp]
        JsonData = {"GrpId":GrpId,"GroupName":Grp,"LiId":LiID,"NewStatus":NewStatus}
        #IsVersionSupported,CallType,ApiUri,Headers,Body = get_group_update_resources(CRVERSION,sessionname,TOKEN,LiID,GrpId,Grp,NewStatus)
        json_object = StdAPIUtils.generic_api_call_handler_no_post(outputFormat,sessionname,get_group_update_resources,JsonData)

        Success = False
        CurentStatus = 'no change'
        GroupNumber = Grp
        if('success' in json_object):
            Success = json_object['success']
        if('data' in json_object):
            CurentStatus = json_object['data']
        aRow = {'GroupNumber':GroupNumber,'CurrentState':CurentStatus,'GroupID':GrpId,'UpdateSuccess':Success}
        AllRows.append(aRow)

    FinalDF = pd.DataFrame(AllRows)
    if (outputFormat == "DF"):
        print(FinalDF)
    elif (outputFormat == "CSV"):
        print(FinalDF.to_csv(index=False))
    else:
        print(FinalDF.to_json())
