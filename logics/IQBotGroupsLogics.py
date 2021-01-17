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

def get_group_list_resources(crversion,sessionname,token):

    if (crversion == "A2019.18"):
        Headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'x-authorization': token
        }

        api_op = "/IQBot/api/bots"
        api_call_type = "GET"

        return True,api_call_type,api_op,Headers,None
    else:
        return False,None,None,None,None

def list_groups(outputFormat,sessionname):

    url = DataUtils.GetUrl(sessionname)
    TOKEN = DataUtils.GetAuthToken(sessionname)
    CRVERSION = DataUtils.GetCRVersion(sessionname)

    IsVersionSupported,CallType,ApiUri,Headers,Body = get_group_list_resources(CRVERSION,sessionname,TOKEN)

    if not IsVersionSupported:
        logging.debug("Unsupported CR Version: {}".format(crversion))
        print("Unsupported CR Version")
        exit(1)

    FULLURL = urllib.parse.urljoin(url,ApiUri)

    response = requests.request(method=CallType, url=FULLURL, data=Body, headers=Headers)

    isAPICallOK = StdResponses.processAPIResponse(response)
    #print(response.text)
    if(not isAPICallOK):
        exit(99)
    else:
        json_object = json.loads(response.text)
        if (outputFormat == "DF"):
            #print(json_object)
            aDF = IQBotGroupTransformers.GetGroupListAsCsv(json_object)
            print(aDF)
        elif (outputFormat == "CSV"):
            #print(json_object)
            aDF = IQBotGroupTransformers.GetGroupListAsCsv(json_object)
            print(aDF.to_csv(index=False))
        else:
            #print(json_object)
            json_formatted_str = json.dumps(json_object, indent=2)
            print(json_formatted_str)

#LI_GROUP_LIST_REQ_TYPE = "POST"
#LI_GROUP_LIST_URI = "/IQBot/api/bots"


def get_group_update_resources(crversion,sessionname,token,LiID,GroupID,GroupNumber,NewStatus):
    VALIDACTIONS = ['ON','OFF']
    if (crversion == "A2019.18"):
        Headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'x-authorization': token
        }
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

        #print("BODY:"+str(Body))
        api_op = "/IQBot/api/projects/"+LiID+"/categories/"+GroupNumber+"/bots/"+GroupID+"/state"
        api_call_type = "POST"
        return True,api_call_type,api_op,Headers,Body
    else:
        return False,None,None,None,None

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
        IsVersionSupported,CallType,ApiUri,Headers,Body = get_group_update_resources(CRVERSION,sessionname,TOKEN,LiID,GrpId,Grp,NewStatus)

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
