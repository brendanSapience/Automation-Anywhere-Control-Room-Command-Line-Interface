import requests
import json
import sys
import os
import urllib.parse

sys.path.insert(1, './libs')
sys.path.insert(1, './responses')
import DataUtils
import IQBotLIResponses
import IQBotCommons

LI_LIST_URI = "/IQBot/api/projects"
LI_LIST_REQ_TYPE = "GET"

LI_FILE_LIST_PER_STATUS_REQ_TYPE = "GET"
# VALIDATION, INVALID, SUCCESS, UNCLASSIFIED, UNTRAINED
def get_LI_FILE_LIST_PER_STATUS_URI(LIID,STATUS):
    ValidStatuses = ['VALIDATION', 'INVALID', 'SUCCESS', 'UNCLASSIFIED', 'UNTRAINED']
    if STATUS.upper() not in ValidStatuses:
        print("Error: Invalid File Status: "+STATUS)
        exit(1)

    return "/IQBot/gateway/learning-instances/"+LIID+"/files/list?docStatus="+STATUS.upper()

LI_DETAIL_REQ_TYPE = "GET"
def get_LI_DETAIL_URI(LIID):
    return "/IQBot/api/projects/"+LIID+"/detail-summary"

LI_FILE_LIST_REQ_TYPE = "GET"
def get_LI_FILE_LIST_URI(LIID):
    return "/IQBot/api/projects/"+LIID+"/files"

LI_GROUP_LIST_REQ_TYPE = "GET"
def get_LI_GROUP_LIST_URI(LIID):
    #/IQBot/api/projects/4a505399-e0d5-45b4-ac18-ac88a1d9763a/categories?offset=0&limit=50&sort=-index&trainingNotRequired=true
    return "/IQBot/api/projects/"+LIID+"/categories?offset=0&limit=50&sort=-index"

def get_learning_instance_detail(learningInstanceName = "",learningInstanceID = "",sessionname = "",CsvOutput = False,ProcessOutput = True):

    if(learningInstanceName != ""):
        learningInstanceID = IQBotCommons.ConvertLINameToLIID(sessionname,learningInstanceName)

    URL = urllib.parse.urljoin(DataUtils.GetUrl(sessionname), get_LI_DETAIL_URI(learningInstanceID))

    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'X-Authorization': DataUtils.GetAuthToken(sessionname)
    }

    response = requests.request(LI_DETAIL_REQ_TYPE, URL, headers=headers)
    if(ProcessOutput):
        isInError = IQBotLIResponses.Process_LI_Detail_Response(response,CsvOutput)
    else:
        return response

def list_learning_instance_files(learningInstanceName = "",learningInstanceID = "",status="",sessionname = "",CsvOutput = False,ProcessOutput = True):

    if(learningInstanceName != ""):
        learningInstanceID = IQBotCommons.ConvertLINameToLIID(sessionname,learningInstanceName)

    if(status == ""):
        URL = urllib.parse.urljoin(DataUtils.GetUrl(sessionname), get_LI_FILE_LIST_URI(learningInstanceID))
        #print(URL)
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'X-Authorization': DataUtils.GetAuthToken(sessionname)
        }

        response = requests.request(LI_FILE_LIST_REQ_TYPE, URL, headers=headers)
        if(ProcessOutput):
            isInError = IQBotLIResponses.Process_File_List_Response(response,CsvOutput)
        else:
            return response

    else:

        URL = urllib.parse.urljoin(DataUtils.GetUrl(sessionname), get_LI_FILE_LIST_PER_STATUS_URI(learningInstanceID,status))
        #print(URL)
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'X-Authorization': DataUtils.GetAuthToken(sessionname)
        }

        response = requests.request(LI_FILE_LIST_PER_STATUS_REQ_TYPE, URL, headers=headers)
        if(ProcessOutput):
            isInError = IQBotLIResponses.Process_LI_Files_With_Status_Response(response,CsvOutput)
        else:
            return response


def list_learning_instance_groups(learningInstanceName = "",learningInstanceID = "",sessionname = "",CsvOutput = False,ProcessOutput = True):

    if(learningInstanceName != ""):
        learningInstanceID = IQBotCommons.ConvertLINameToLIID(sessionname,learningInstanceName)

    URL = urllib.parse.urljoin(DataUtils.GetUrl(sessionname), get_LI_GROUP_LIST_URI(learningInstanceID))

    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'X-Authorization': DataUtils.GetAuthToken(sessionname)
    }

    response = requests.request(LI_GROUP_LIST_REQ_TYPE, URL, headers=headers)
    if(ProcessOutput):
        isInError = IQBotLIResponses.Process_Group_List_Response(response,CsvOutput)
    else:
        return response

def list_learning_instances(sessionname,CsvOutput,ProcessOutput = True):
    return IQBotCommons.list_learning_instances(sessionname,CsvOutput,ProcessOutput)
