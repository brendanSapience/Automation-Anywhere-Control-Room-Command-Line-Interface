import json
import pandas as pd
from pandas.io.json import json_normalize

def GetCsvCredsList(jsonResults):

    myDF = pd.DataFrame(jsonResults['list'])
    myDF.pop('attributes')

    return myDF

def GetCsvCredsShow(jsonResults):

    myDF = pd.DataFrame(jsonResults)

    return myDF
