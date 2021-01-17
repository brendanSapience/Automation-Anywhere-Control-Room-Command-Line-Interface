import requests
import json
import sys
import os
import urllib.parse

sys.path.insert(1, './libs')
sys.path.insert(1, './responses')
import DataUtils
import StdResponses
import AuthResponses
import logging

def get_login_resources(crversion, login, password, sessionname):

    if (crversion == "A2019.18"):
        body = json.dumps(
            {
                'username': login,
                'password':password
            }
        )

        api_op = "/v1/authentication"
        api_call_type = "POST"

        Headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }

        return True,api_call_type,api_op,Headers,body
    else:
        return False,None,None,None,None

def login(crversion,url,login,password,sessionname):

    IsVersionSupported,CallType,ApiUri,Headers,Body = get_login_resources(crversion,login,password,sessionname)

    if not IsVersionSupported:
        logging.debug("Unsupported CR Version: {}".format(crversion))
        print("Unsupported CR Version")
        exit(1)

    FULLURL = urllib.parse.urljoin(url,ApiUri)

    response = requests.request(CallType, FULLURL, data=Body, headers=Headers)

    isAPICallOK = StdResponses.processAPIResponse(response)
    if(not isAPICallOK):
        exit(99)
    else:
        #print("DEBUG"+str(response.text))
        isError,Code = AuthResponses.Process_Auth_Login_Response(response)
        if(not isError):
            DataUtils.StoreAuthToken(Code,sessionname)
            DataUtils.StoreUrl(url,sessionname)
            DataUtils.StoreCRVersion(crversion,sessionname)
            print("Token Stored in session: "+sessionname)

def logout(sessionname):
    DataUtils.DeleteSessionFiles(sessionname)
    print("Session deleted: "+sessionname)

def listSessions():
    SessionList,IsError = DataUtils.listSessions()
    if(IsError):
        print("Error retrieving session list.")
    else:
        print(SessionList)
