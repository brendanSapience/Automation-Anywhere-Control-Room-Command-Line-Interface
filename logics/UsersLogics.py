import requests
import json
import sys
import os
import urllib.parse
import pandas as pd

sys.path.insert(1, './libs')
sys.path.insert(1, './transformers')
sys.path.insert(1, './responses')
import DataUtils
import UsersTransformers
import StdResponses
import StdAPIUtils

def get_user_delete_resources(crversion,sessionname,token,JsonData):
    Headers = StdAPIUtils.get_api_call_headers(crversion,token)
    UserId = JsonData['userId']

    if (crversion == "A2019.18"):

        api_op = "/v1/usermanagement/users/"+UserId
        api_call_type = "DELETE"

        return True,api_call_type,api_op,Headers,None
    else:
        return False,None,None,None,None
def ConvertUsernameToList(username):
    if("," in username):
        return username.split(",")
    else:
        return [username]

def get_user_setlogin_resources(crversion,sessionname,token,JsonData):
    Headers = StdAPIUtils.get_api_call_headers(crversion,token)

    username = JsonData['username']
    loginuser = JsonData['loginuser']
    loginpassword = JsonData['loginpassword']

    if (crversion == "A2019.18"):

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

def get_user_list_resources(crversion,sessionname,token,JsonData):

    Headers = StdAPIUtils.get_api_call_headers(crversion,token)

    if (crversion == "A2019.18"):

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

def get_user_create_resources(crversion,sessionname,token,JsonData):

    Headers = StdAPIUtils.get_api_call_headers(crversion,token)
    username = JsonData['username']
    password = JsonData['password']
    email = JsonData['email']
    description = JsonData['desc']
    firstname = JsonData['firstname']
    lastname = JsonData['lastname']
    roles = GET_ID_AS_JSON(JsonData['roles'])

    if (crversion == "A2019.18"):

        api_op = "/v1/usermanagement/users"
        api_call_type = "POST"

        Body = b = json.dumps(

        {
            "roles":roles,
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

        #["RUNTIME", "DISCOVERYBOTANALYZER", "DISCOVERYBOTRECORDER", "AARIUSER", "ANALYTICSCLIENT"]
        altLicFeatures = [
        "DEVELOPMENT", #'ATTENDEDRUNTIME' (attended), 'RUNTIME' (unattended), 'DEVELOPMENT' (bot creator)
        "DISCOVERYBOTANALYZER",
        "DISCOVERYBOTRECORDER",
        "AARIUSER",
        "ANALYTICSCLIENT"
        ]


        return True,api_call_type,api_op,Headers,Body
    else:
        return False,None,None,None,None


def get_user_delete_resources(crversion,sessionname,token,JsonData):
    Headers = StdAPIUtils.get_api_call_headers(crversion,token)
    UserId = JsonData['userId']
    if (crversion == "A2019.18"):

        api_op = "/v1/usermanagement/users/"+UserId
        api_call_type = "DELETE"

        return True,api_call_type,api_op,Headers,None
    else:
        return False,None,None,None,None
def ConvertUsernameToList(username):
    if("," in username):
        return username.split(",")
    else:
        return [username]

def ConvertUsernameToListOfIDs(outputFormat,username,sessionname):
    ListOfUsernames = username.lower().split(",")
    Mappings = {}
    try:
        JsonListOfUsers = StdAPIUtils.generic_api_call_handler_no_post(outputFormat,sessionname,get_user_list_resources,{})

        UserList = JsonListOfUsers['list']
        for item in UserList:
            ID = item['id']
            USERNAME = item['username']
            if(USERNAME in ListOfUsernames):
                Mappings[USERNAME] = ID
        #print(Mappings)
        return Mappings
    except Exception as e:
        print("An error occured while retrieving the list of existing users:"+str(e))
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
    StdAPIUtils.generic_api_call_handler(outputFormat,sessionname,get_user_list_resources,{},UsersTransformers.GetUserListAsCsv)

#args.OUTPUTFORMAT,args.sessionname,args.USERNAME,args.PASSWORD,args.EMAIL,args.ROLES,args.DESC,args.FIRSTNAME,args.LASTNAME
def create(outputFormat,sessionname,username,password,email,roles,description,firstname,lastname):

    AllUsernames = ConvertUsernameToList(username)

    AllRows = []

    for aUser in  AllUsernames:
        JsonData = {
        "username":username,
        "password":password,
        "email":email,
        "roles":roles,
        "desc":description,
        "firstname":firstname,
        "lastname":lastname
        }
        json_object = StdAPIUtils.generic_api_call_handler_no_post(outputFormat,sessionname,get_user_create_resources,JsonData)

        Success = False

        if('id' in json_object):
            Success = True
            aRow = {'id':json_object['id'],'username':json_object['username'],'success':Success}
        else:
            aRow = {'id':"",'username':"",'success':Success}

        AllRows.append(aRow)

    FinalDF = pd.DataFrame(AllRows)
    if (outputFormat == "DF"):
        print(FinalDF)
    elif (outputFormat == "CSV"):
        print(FinalDF.to_csv(index=False))
    else:
        print(FinalDF.to_json())

def delete(outputFormat,sessionname,username):
    # delete API endpoint only takes the user id and not the user Name
    # all usernames passed need to be first converted to a list of user ids
    AllRows = []

    AllUsernames = ConvertUsernameToListOfIDs(outputFormat,username,sessionname)

    for username,userid in  AllUsernames.items():
        JsonData = {"userId":str(userid)}
        json_object = StdAPIUtils.generic_api_call_handler_no_post(outputFormat,sessionname,get_user_delete_resources,JsonData)

        Success = False

        if('id' in json_object):
            Success = True
            aRow = {'id':json_object['id'],'username':json_object['username'],'success':Success}
        else:
            aRow = {'id':"",'username':"",'success':Success}

        AllRows.append(aRow)

    FinalDF = pd.DataFrame(AllRows)
    if (outputFormat == "DF"):
        print(FinalDF)
    elif (outputFormat == "CSV"):
        print(FinalDF.to_csv(index=False))
    else:
        print(FinalDF.to_json())


def setlogin(outputFormat,sessionname,username,loginuser,loginpassword):
    AllUsernames = ConvertUsernameToList(username)

    AllRows = []

    for aUser in AllUsernames:
        JsonData = {"username":str(aUser).lower(),"loginuser":loginuser,"loginpassword":loginpassword}
        json_object = StdAPIUtils.generic_api_call_handler_no_post(outputFormat,sessionname,get_user_setlogin_resources,JsonData)
        RawResponse = str(json_object)

        Success = False
        if('updated' in RawResponse): #this is a weird one.. upon update, the API returns a single string "Credentials updated for ausertocreate"
            Success = True

        aRow = {'username':str(aUser).lower(),'success':Success}

        AllRows.append(aRow)

    FinalDF = pd.DataFrame(AllRows)
    if (outputFormat == "DF"):
        print(FinalDF)
    elif (outputFormat == "CSV"):
        print(FinalDF.to_csv(index=False))
    else:
        print(FinalDF.to_json())
