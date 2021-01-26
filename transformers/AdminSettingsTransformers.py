import json
import pandas as pd
from pandas.io.json import json_normalize

def GetCsvAdminPwdShow(jsonResults):

    myDF = pd.DataFrame(jsonResults)

    return myDF
