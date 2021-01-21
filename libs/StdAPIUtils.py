import requests
import json
import sys
import os
import urllib.parse
sys.path.insert(1, './libs')
sys.path.insert(1, './responses')
sys.path.insert(1, './transformers')
import DataUtils
import StdResponses

def get_api_call_headers(crversion,token):
    DefaultHeaders = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'X-Authorization': token
    }

    if(crversion == "A2019.18"):
        Headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'X-Authorization': token
        }
        return Headers

    return DefaultHeaders

# Generic API Handler with embedded processing of Output
def generic_api_call_handler(outputFormat,sessionname,get_res_func,res_data,df_transform_func):
        url = DataUtils.GetUrl(sessionname)
        TOKEN = DataUtils.GetAuthToken(sessionname)
        CRVERSION = DataUtils.GetCRVersion(sessionname)

        IsVersionSupported,CallType,ApiUri,Headers,Body = get_res_func(CRVERSION,sessionname,TOKEN,res_data)

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
                aDF = df_transform_func(json_object)
                print(aDF)
            elif (outputFormat == "CSV"):
                #print(json_object)
                aDF = df_transform_func(json_object)
                print(aDF.to_csv(index=False))
            else:
                #print(json_object)
                json_formatted_str = json.dumps(json_object, indent=2)
                print(json_formatted_str)

# Generic API Handler with no processing of Output
def generic_api_call_handler_no_post(outputFormat,sessionname,get_res_func,res_data):
        url = DataUtils.GetUrl(sessionname)
        TOKEN = DataUtils.GetAuthToken(sessionname)
        CRVERSION = DataUtils.GetCRVersion(sessionname)

        IsVersionSupported,CallType,ApiUri,Headers,Body = get_res_func(CRVERSION,sessionname,TOKEN,res_data)

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
            if(response.text != ""):
                json_object = json.loads(response.text)
                return json_object
            else:
                return response.status_code
