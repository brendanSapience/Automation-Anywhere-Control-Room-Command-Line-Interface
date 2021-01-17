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

def get_li_file_list_per_status_resources(crversion,sessionname,token,LiId,Status):
    ValidStatuses = ['VALIDATION', 'INVALID', 'SUCCESS', 'UNCLASSIFIED', 'UNTRAINED']

    if (crversion == "A2019.18"):
        Headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'X-Authorization': token
        }

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

def get_li_grp_list_resources(crversion,sessionname,token,LiId):

    if (crversion == "A2019.18"):
        Headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'X-Authorization': token
        }

        api_op = "/IQBot/api/projects/"+LiId+"/categories?offset=0&limit=50&sort=-index&trainingNotRequired=true"
        api_call_type = "GET"

        return True,api_call_type,api_op,Headers,None
    else:
        return False,None,None,None,None

def get_learning_instance_detail(outputFormat,sessionname,LiId):

    url = DataUtils.GetUrl(sessionname)
    TOKEN = DataUtils.GetAuthToken(sessionname)
    CRVERSION = DataUtils.GetCRVersion(sessionname)

    IsVersionSupported,CallType,ApiUri,Headers,Body = get_li_detail_resources(CRVERSION,sessionname,TOKEN,LiId)

    if not IsVersionSupported:
        logging.debug("Unsupported CR Version: {}".format(crversion))
        print("Unsupported CR Version")
        exit(1)

    FULLURL = urllib.parse.urljoin(url,ApiUri)
    print(FULLURL)
    print(CallType)
    print(Headers)

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

def list_learning_instance_files(outputFormat,sessionname,LiId, Status):

    url = DataUtils.GetUrl(sessionname)
    TOKEN = DataUtils.GetAuthToken(sessionname)
    CRVERSION = DataUtils.GetCRVersion(sessionname)

    if(Status == ""):
        IsVersionSupported,CallType,ApiUri,Headers,Body = get_li_file_list_resources(CRVERSION,sessionname,TOKEN,LiId)
    else:
        IsVersionSupported,CallType,ApiUri,Headers,Body = get_li_file_list_per_status_resources(CRVERSION,sessionname,TOKEN,LiId,Status)

    if not IsVersionSupported:
        logging.debug("Unsupported CR Version: {}".format(crversion))
        print("Unsupported CR Version")
        exit(1)

    FULLURL = urllib.parse.urljoin(url,ApiUri)

    response = requests.request(method=CallType, url=FULLURL, data=Body, headers=Headers)
    #print(response.text)
    isAPICallOK = StdResponses.processAPIResponse(response)
    if(not isAPICallOK):
        exit(99)
    else:
        json_object = json.loads(response.text)
        #print(json_object)
        if Status == "":
            aDF = IQBotLITransformers.GetLIFileListAsCsv(json_object)
            if(outputFormat == "DF"):
                print(aDF)
            elif(outputFormat == "CSV"):
                print(aDF.to_csv(index=False))
            else:
                json_formatted_str = json.dumps(json_object, indent=2)
                print(json_formatted_str)
        else:

            aDF = IQBotLITransformers.GetFileListPerStatusAsCsv(json_object)
            if(outputFormat == "DF"):
                print(aDF)
            elif(outputFormat == "CSV"):
                print(aDF.to_csv(index=False))
            else:
                json_formatted_str = json.dumps(json_object, indent=2)
                print(json_formatted_str)


def list_learning_instance_groups(outputFormat,sessionname,LiId):

    url = DataUtils.GetUrl(sessionname)
    TOKEN = DataUtils.GetAuthToken(sessionname)
    CRVERSION = DataUtils.GetCRVersion(sessionname)

    IsVersionSupported,CallType,ApiUri,Headers,Body = get_li_grp_list_resources(CRVERSION,sessionname,TOKEN,LiId)

    if not IsVersionSupported:
        logging.debug("Unsupported CR Version: {}".format(crversion))
        print("Unsupported CR Version")
        exit(1)

    FULLURL = urllib.parse.urljoin(url,ApiUri)
    #print(FULLURL)
    #print(CallType)
    #print(Headers)

    response = requests.request(method=CallType, url=FULLURL, data=Body, headers=Headers)

    isAPICallOK = StdResponses.processAPIResponse(response)
    if(not isAPICallOK):
        exit(99)
    else:
        json_object = json.loads(response.text)
        if (outputFormat == "DF"):
            #print(json_object)
            aDF = IQBotLITransformers.GetLIGroupListAsCsv(json_object)
            print(aDF)
        elif (outputFormat == "CSV"):
            #print(json_object)
            aDF = IQBotLITransformers.GetLIGroupListAsCsv(json_object)
            print(aDF.to_csv(index=False))
        else:
            #print(json_object)
            json_formatted_str = json.dumps(json_object, indent=2)
            print(json_formatted_str)
