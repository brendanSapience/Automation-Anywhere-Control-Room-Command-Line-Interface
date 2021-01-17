import requests
import json
import sys
import os
import urllib.parse

sys.path.insert(1, './libs')
sys.path.insert(1, './responses')
import DataUtils
import IQBotGroupResponses
import IQBotCommons

VALIDACTIONS = ['activate','deactivate']

LI_GROUP_LIST_URI = "/IQBot/api/bots"
LI_GROUP_LIST_REQ_TYPE = "GET"

LI_GROUP_LIST_REQ_TYPE = "POST"
LI_GROUP_LIST_URI = "/IQBot/api/bots"

LI_GROUP_CHANGE_STATE_REQ_TYPE = "POST"
def get_LI_GROUP_CHANGE_STATE_URI(LIID,GROUPID, GROUPNUMBER):
    #IQBot/api/projects/4a505399-e0d5-45b4-ac18-ac88a1d9763a/categories/8/bots/8c2f9553-6c04-40da-aa45-2116716d3f38/state
    return "/IQBot/api/projects/"+LIID+"/categories/"+GROUPNUMBER+"/bots/"+GROUPID+"/state"

def GET_GROUP_CHANGE_STATE_BODY(Action): #staging or production
    NewState = ""
    if(Action.lower() in VALIDACTIONS):
        if(Action.lower() == VALIDACTIONS[0]):
            NewState = 'production'

        if(Action.lower() == VALIDACTIONS[1]):
            NewState = 'staging'

        b = json.dumps(
            {
            "state":
            NewState.lower()
            }
        )
        #print(b)
        return b
    else:
        print("Error: Group State Invalid: "+NewState.lower())
        exit(1)

def list_groups(sessionname,CsvOutput,ProcessOutput = True):
    URL = urllib.parse.urljoin(DataUtils.GetUrl(sessionname), LI_GROUP_LIST_URI)

    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'X-Authorization': DataUtils.GetAuthToken(sessionname)
    }

    response = requests.request(LI_GROUP_LIST_REQ_TYPE, URL, headers=headers)

    if(ProcessOutput):
        isInError = IQBotGroupResponses.Process_List_Response(response,CsvOutput)

    else:
        return response

def change_group(groupnum,liname,operation,sessionname,CsvOutput,ProcessOutput = True):

    liid,groupMappings = IQBotCommons.GetAllGroupsFromLI(sessionname,liname)

    AllGroups = []
    if("," in groupnum):
        AllGroups = groupnum.split(",")
    elif(groupnum.upper() in ["ALL","ALLGROUPS","ALLGRPS","EVERYTHING"]):
        AllGroups = list(groupMappings.keys())
    else:
        AllGroups.append(groupnum)


    for Grp in AllGroups:
        GrpId = groupMappings[Grp]
        URL = urllib.parse.urljoin(DataUtils.GetUrl(sessionname), get_LI_GROUP_CHANGE_STATE_URI(liid,GrpId,Grp))
        payload = GET_GROUP_CHANGE_STATE_BODY(operation)
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'X-Authorization': DataUtils.GetAuthToken(sessionname)
        }

        response = requests.request(LI_GROUP_CHANGE_STATE_REQ_TYPE, URL,data=payload, headers=headers)
        #print(response.text)
        if(ProcessOutput):
            isInError = IQBotGroupResponses.Process_Grp_State_Change_Response(response,Grp,liname,CsvOutput)

        else:
            return response
