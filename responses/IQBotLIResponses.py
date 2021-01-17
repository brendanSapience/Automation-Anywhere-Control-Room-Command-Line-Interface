import requests
import json
import sys
import os

sys.path.insert(1, './libs')
sys.path.insert(1, './transformers')
import DataUtils
import IQBotLITransformers
import StdResponses

def Process_LI_Files_With_Status_Response(res,CsvOutput):
    isError,isCsvOutput = StdResponses.ProcessStdResponse(res,CsvOutput)
    if(isError):
        exit(1)
    else:
        result = json.loads(res.text)
        if isCsvOutput:
            print(IQBotLITransformers.GetFileListPerStatusAsCsv(result))
            exit(0)
        else:
            print(result)
            exit(0)

def Process_Group_List_Response(res,CsvOutput):
    isError,isCsvOutput = StdResponses.ProcessStdResponse(res,CsvOutput)
    if(isError):
        exit(1)
    else:
        result = json.loads(res.text)
        if isCsvOutput:
            print(IQBotLITransformers.GetLIDetailAsCsv(result))
            exit(0)
        else:
            print(result)
            exit(0)

def Process_Group_List_Response(res,CsvOutput):
    isError,isCsvOutput = StdResponses.ProcessStdResponse(res,CsvOutput)
    if(isError):
        exit(1)
    else:
        result = json.loads(res.text)
        if isCsvOutput:
            print(IQBotLITransformers.GetLIGroupListAsCsv(result))
            exit(0)
        else:
            print(result)
            exit(0)

def Process_File_List_Response(res,CsvOutput):
    isError,isCsvOutput = StdResponses.ProcessStdResponse(res,CsvOutput)
    if(isError):
        exit(1)
    else:
        result = json.loads(res.text)
        if isCsvOutput:
            print(IQBotLITransformers.GetLIFileListAsCsv(result))
            exit(0)
        else:
            print(result)
            exit(0)

def Process_List_Response(res,CsvOutput):
    isError,isCsvOutput = StdResponses.ProcessStdResponse(res,CsvOutput)
    if(isError):
        exit(1)
    else:
        result = json.loads(res.text)
        if isCsvOutput:
            print(IQBotLITransformers.GetLIListAsCsv(result))
            exit(0)
        else:
            print(result)
            exit(0)
