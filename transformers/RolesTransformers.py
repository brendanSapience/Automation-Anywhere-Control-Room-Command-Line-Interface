import json
import pandas as pd

def GetListAsCsv(jsonResults):

    AllRows = []

    out_df = pd.DataFrame(columns=['id','name','description','countPrincipals','version','createdBy','createdOn','updatedBy','updatedOn'])

    ItemList = jsonResults['list']
    for item in ItemList:
        ID = item['id']
        NAME = item['name']
        DESC = item['description']
        COUNT = item['countPrincipals']
        VERSION = item['version']
        CREATEDBY = item['createdBy']
        CREATEDON = item['createdOn']
        UPDATEDBY = item['updatedBy']
        UPDATEDON = item['updatedOn']
        #,'updatedBy':UPDATEDBY,'updatedOn':UPDATEDON
        new_row = {'id':ID,'name':NAME,'description':DESC,'countPrincipals':COUNT,'version':VERSION,'createdBy':CREATEDBY,'createdOn':CREATEDON}
        AllRows.append(new_row)

    FinalDF = pd.DataFrame(AllRows)
    return FinalDF
