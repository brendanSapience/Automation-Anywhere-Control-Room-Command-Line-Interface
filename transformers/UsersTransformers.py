import json
import pandas as pd

def GetUserListAsCsv(jsonResults):

    AllRows = []

    out_df = pd.DataFrame(columns=['id','username','domain','firstName','lastName','version','principalId',
        'email','passwordSet','questionsSet','disabled','description','createdOn'])

    ItemList = jsonResults['list']
    for item in ItemList:
        ID = item['id']
        USERNAME = item['username']
        DOMAIN = item['domain']
        FIRSTNAME = item['firstName']
        LASTNAME = item['lastName']
        VERSION = item['version']
        PRINCIPALID = item['principalId']
        EMAIL = item['email']
        PASSWORDSET = item['passwordSet']
        QUESTIONSSET = item['questionsSet']
        DISABLED = item['disabled']
        DESC = item['description']
        CREATEDON = item['createdOn']

        new_row = {'id':ID,'username':USERNAME,'domain':DOMAIN,'firstName':FIRSTNAME,'lastName':LASTNAME,'version':VERSION,
            'principalId':PRINCIPALID,'email':EMAIL,'passwordSet':PASSWORDSET,'questionsSet':QUESTIONSSET,'disabled':DISABLED,'description':DESC,'createdOn':CREATEDON}
        AllRows.append(new_row)

    FinalDF = pd.DataFrame(AllRows)
    return FinalDF
