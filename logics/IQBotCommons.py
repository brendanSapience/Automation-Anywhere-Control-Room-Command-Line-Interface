import requests
import json
import sys
import os
import urllib.parse
sys.path.insert(1, './responses')
import DataUtils
import IQBotLIResponses

LI_LIST_URI = "/IQBot/api/projects"
LI_LIST_REQ_TYPE = "GET"

LI_LIST_GROUPS_FROM_LI = "GET"
def get_LI_LIST_GROUPS_FROM_LI_URI(LIID):
    # /IQBot/api/projects/b069d79d-5df0-43dc-824f-2c44474867ca/categories?offset=0&limit=50&sort=-index&trainingNotRequired=true
    return "/IQBot/api/projects/"+LIID+"/categories?offset=0&limit=5000&sort=-index&trainingNotRequired=true"


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



def GetAllGroupsFromLI(sessionname,liname):
    Mappings = {}
    try:

        liid = ConvertLINameToLIID(sessionname,liname)
        res = list_groups_from_li(liid,sessionname)
        #print(res.text)
        JsonList = json.loads(res.text)
        #print(res)
        ItemList = JsonList['data']['categories']
        #print(ItemList)
        for item in ItemList:

            ID = item['id']
            NAME = item['name']
            GRPID = item['visionBot']['id']
            Mappings[ID] = GRPID

        return liid,Mappings
    except:
        print("An error occured while converting getting Group List for LI.")
        exit(1)

def list_groups_from_li(liid,sessionname):
    # /IQBot/api/projects/b069d79d-5df0-43dc-824f-2c44474867ca/categories?offset=0&limit=50&sort=-index&trainingNotRequired=true
    URL = urllib.parse.urljoin(DataUtils.GetUrl(sessionname), get_LI_LIST_GROUPS_FROM_LI_URI(liid))

    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'X-Authorization': DataUtils.GetAuthToken(sessionname)
    }

    response = requests.request(LI_LIST_GROUPS_FROM_LI, URL, headers=headers)
    return response
    #if(ProcessOutput):
    #    isInError = IQBotGroupResponses.Process_LI_Group_List_Response(response,CsvOutput)
    #else:
    #    return response

def list_learning_instances(sessionname,CsvOutput,ProcessOutput = True):
    URL = urllib.parse.urljoin(DataUtils.GetUrl(sessionname), LI_LIST_URI)

    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'X-Authorization': DataUtils.GetAuthToken(sessionname)
    }

    response = requests.request(LI_LIST_REQ_TYPE, URL, headers=headers)

    if(ProcessOutput):
        isInError = IQBotLIResponses.Process_List_Response(response,CsvOutput)

    else:
        return response
