import requests
import json
import sys
import os
import urllib.parse

sys.path.insert(1, './libs')
sys.path.insert(1, './transformers')
sys.path.insert(1, './responses')
import DataUtils
import UsersTransformers
import StdResponses

def get_user_setlogin_resources(crversion,sessionname,token):

    if (crversion == "A2019.18"):
        Headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'X-Authorization': token
        }


        api_op = "/v2/credentialvault/loginsetting"
        api_call_type = "PUT"

        Body = b = json.dumps(
        {
            "username":username,
            "loginUsername":loginuser,
            "loginPassword":loginpassword
        }
        )

        return True,api_call_type,api_op,Headers,Body
    else:
        return False,None,None,None,None

def get_user_list_resources(crversion,sessionname,token):

    if (crversion == "A2019.18"):
        Headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'X-Authorization': token
        }


        api_op = "/v1/usermanagement/users/list"
        api_call_type = "POST"

        Body = b = json.dumps(
        {
        "sort":[
            {"field":"username",
            "direction":"asc"}
        ],
        "filter":{},
        "fields":[],
        "page":{
            "offset":0,
            "total":12,
            "totalFilter":12,
            "length":200
            }
        }
        )

        return True,api_call_type,api_op,Headers,Body
    else:
        return False,None,None,None,None

def get_user_create_resources(crversion,sessionname,token):

    if (crversion == "A2019.18"):
        Headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'X-Authorization': token
        }


        api_op = "/v1/usermanagement/users"
        api_call_type = "POST"

        Body = b = json.dumps(

        {
            "roles":GET_ID_AS_JSON(roles),
            "email":email,
            "enableAutoLogin":True,
            "username":username,
            "description":description,
            "firstName":firstname,
            "lastName":lastname,
            "disabled":False,
            "password":password,
            "licenseFeatures":["DEVELOPMENT"],
            "sysAssignedRoles":[]
        }
        )

        return True,api_call_type,api_op,Headers,Body
    else:
        return False,None,None,None,None

USER_DELETE_URI = "/v1/usermanagement/users"
USER_DELETE_REQ_TYPE = "DELETE"

def ConvertUsernameToList(username):
    if("," in username):
        return username.split(",")
    else:
        return [username]

def ConvertUsernameToListOfIDs(username,sessionname):
    ListOfUsernames = username.split(",")
    Mappings = {}
    try:
        res = list(sessionname,False,False)
        JsonListOfUsers = json.loads(res.text)

        UserList = JsonListOfUsers['list']
        for item in UserList:
            ID = item['id']
            USERNAME = item['username']
            if(USERNAME in ListOfUsernames):
                Mappings[USERNAME] = ID
        #print(Mappings)
        return Mappings
    except:
        print("An error occured while retrieving the list of existing users.")
        exit(1)

def GET_ID_AS_JSON(roles):
    try:
        allRoles = roles.split(",")
        allRolesJson = []
        for role in allRoles:
            e ={"id":int(role)}
            allRolesJson.append(e)
        return allRolesJson
    except:
        print("Error: list of roles isnt formatted correctly.")
        exit(1)

def user_list(outputFormat,sessionname):

    url = DataUtils.GetUrl(sessionname)
    TOKEN = DataUtils.GetAuthToken(sessionname)
    CRVERSION = DataUtils.GetCRVersion(sessionname)

    IsVersionSupported,CallType,ApiUri,Headers,Body = get_user_list_resources(CRVERSION,sessionname,TOKEN)

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
            aDF = UsersTransformers.GetUserListAsCsv(json_object)
            print(aDF)
        elif (outputFormat == "CSV"):
            #print(json_object)
            aDF = UsersTransformers.GetUserListAsCsv(json_object)
            print(aDF.to_csv(index=False))
        else:
            #print(json_object)
            json_formatted_str = json.dumps(json_object, indent=2)
            print(json_formatted_str)

    #isInError = RolesResponses.Process_list_Response(response,CsvOutput)

def create(sessionname,username,password,email,roles,description,firstname,lastname):

    AllUsernames = ConvertUsernameToList(username)

    for aUser in  AllUsernames:

        URL = urllib.parse.urljoin(DataUtils.GetUrl(sessionname), USER_CREATE_URI)

        payload = GET_USER_CREATE_BODY(aUser,password,email,roles,description,firstname,lastname)
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'X-Authorization': DataUtils.GetAuthToken(sessionname)
        }

        response = requests.request(USER_CREATE_REQ_TYPE, URL, data=payload, headers=headers)
        isInError = UsersResponses.Process_Create_Response(response)



def delete(sessionname,username):
    # delete API endpoint only takes the user id and not the user Name
    # all usernames passed need to be first converted to a list of user ids
    AllUsernames = ConvertUsernameToListOfIDs(username,sessionname)

    for username,userid in  AllUsernames.items():
        URL = urllib.parse.urljoin(DataUtils.GetUrl(sessionname), USERUSER_DELETE_URI,str(userid))
        USER_LIST_URI
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'X-Authorization': DataUtils.GetAuthToken(sessionname)
        }

        response = requests.request(USER_DELETE_REQ_TYPE, URL, headers=headers)
        isInError = UsersResponses.Process_Delete_Response(response)

def setlogin(sessionname,username,loginuser,loginpassword):
    AllUsernames = ConvertUsernameToList(username)

    for aUser in AllUsernames:

        URL = urllib.parse.urljoin(DataUtils.GetUrl(sessionname), USER_SETLOGIN_URI)
        payload = GET_USER_SET_LOGIN_BODY(aUser,loginuser,loginpassword)
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'X-Authorization': DataUtils.GetAuthToken(sessionname)
        }
        #print(payload)
        response = requests.request(USER_SETLOGIN_REQ_TYPE, URL, data=payload, headers=headers)
        isInError = UsersResponses.Process_Set_Login_Response(response)
