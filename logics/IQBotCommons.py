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

def get_li_list_resources(crversion,sessionname,token):

    if (crversion == "A2019.18"):
        Headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'X-Authorization': token
        }


        api_op = "/IQBot/api/projects"
        api_call_type = "GET"

        return True,api_call_type,api_op,Headers,None
    else:
        return False,None,None,None,None


def get_grp_list_from_li_resources(crversion,sessionname,token,LiId):

    if (crversion == "A2019.18"):
        Headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'X-Authorization': token
        }

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

        #liid = ConvertLINameToLIID(sessionname,liname)
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

    url = DataUtils.GetUrl(sessionname)
    TOKEN = DataUtils.GetAuthToken(sessionname)
    CRVERSION = DataUtils.GetCRVersion(sessionname)

    IsVersionSupported,CallType,ApiUri,Headers,Body = get_grp_list_from_li_resources(CRVERSION,sessionname,TOKEN,LiId)

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
        return json_object

def list_groups_from_li(outputFormat,sessionname,LiId):

    url = DataUtils.GetUrl(sessionname)
    TOKEN = DataUtils.GetAuthToken(sessionname)
    CRVERSION = DataUtils.GetCRVersion(sessionname)

    IsVersionSupported,CallType,ApiUri,Headers,Body = get_grp_list_from_li_resources(CRVERSION,sessionname,TOKEN,LiId)

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
        if (outputFormat == "DF"):
            #print(json_object)
            aDF = IQBotLITransformers.GetListAsCsv(json_object)
            print(aDF)
        elif (outputFormat == "CSV"):
            #print(json_object)
            aDF = IQBotLITransformers.GetListAsCsv(json_object)
            print(aDF.to_csv(index=False))
        else:
            #print(json_object)
            json_formatted_str = json.dumps(json_object, indent=2)
            print(json_formatted_str)

    #isInError = RolesResponses.Process_list_Response(response,CsvOutput)

def list_learning_instances(outputFormat,sessionname):

    url = DataUtils.GetUrl(sessionname)
    TOKEN = DataUtils.GetAuthToken(sessionname)
    CRVERSION = DataUtils.GetCRVersion(sessionname)

    IsVersionSupported,CallType,ApiUri,Headers,Body = get_li_list_resources(CRVERSION,sessionname,TOKEN)

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
        if (outputFormat == "DF"):
            #print(json_object)
            aDF = IQBotLITransformers.GetLIListAsCsv(json_object)
            print(aDF)
        elif (outputFormat == "CSV"):
            #print(json_object)
            aDF = IQBotLITransformers.GetLIListAsCsv(json_object)
            print(aDF.to_csv(index=False))
        else:
            #print(json_object)
            json_formatted_str = json.dumps(json_object, indent=2)
            print(json_formatted_str)
