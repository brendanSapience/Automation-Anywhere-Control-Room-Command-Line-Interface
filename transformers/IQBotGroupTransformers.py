import json
import pandas as pd

def GetGroupListAsCsv(jsonResults):

    AllRows = []

    out_df = pd.DataFrame()

    ItemList = jsonResults['data']
    for item in ItemList:
        a1 = item['id']
        #a2 = item['name']
        #a3 = item['organizationId']
        a4 = item['projectId']
        a5 = item['projectName']
        a6 = item['categoryId']
        a7 = item['categoryName']
        #a8 = item['environment']
        a9 = item['status']
        b1 = item['running']
        b2 = item['lastModifiedByUser']
        b3 = item['lastModifiedTimestamp']
        b4 = item['description']
        # = item['']
        # = item['']
        # = item['']
        # = item['']
        # = item['']

        new_row = {
            'id':a1,'LiID':a4,'LIName':a5,'GroupID':a6,'status':a9,
            'running':b1,'lastModifiedByUser':b2,'lastModifiedTimestamp':b3,'description':b4
        }
        AllRows.append(new_row)

    FinalDF = pd.DataFrame(AllRows)
    return FinalDF
