import requests
import json
import sys
import os
import urllib.parse

sys.path.insert(1, './libs')
sys.path.insert(1, './responses')
sys.path.insert(1, './transformers')
import DataUtils
import ActivitiesTransformers
import StdResponses
import StdAPIUtils

def get_audit_list_resources(crversion,sessionname,token):

    if (crversion == "A2019.18"):
        Headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'X-Authorization': token
        }


        api_op = "/v1/audit/messages/list"
        api_call_type = "POST"

        Body = json.dumps(
            {
                "sort": [
                    {
                        "field": "createdOn",
                        "direction": "desc"
                    }
                ],
                "filter": {
                    "operator": "gt",
                    "field": "createdOn",
                    "value": "2020-11-18T20:43:41.030Z"
                },
                "fields": [],
                "page": {
                    "offset": 0,
                    "total": 28865,
                    "totalFilter": 10000,
                    "length": 100
                }
            }
        )

        return True,api_call_type,api_op,Headers,Body
    else:
        return False,None,None,None,None


def activity_list(outputFormat,sessionname):

    url = DataUtils.GetUrl(sessionname)
    TOKEN = DataUtils.GetAuthToken(sessionname)
    CRVERSION = DataUtils.GetCRVersion(sessionname)

    IsVersionSupported,CallType,ApiUri,Headers,Body = get_activity_list_resources(CRVERSION,sessionname,TOKEN)

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
            aDF = ActivitiesTransformers.GetListAsCsv(json_object)
            print(aDF)
        elif (outputFormat == "CSV"):
            #print(json_object)
            aDF = ActivitiesTransformers.GetListAsCsv(json_object)
            print(aDF.to_csv(index=False))
        else:
            #print(json_object)
            json_formatted_str = json.dumps(json_object, indent=2)
            print(json_formatted_str)
