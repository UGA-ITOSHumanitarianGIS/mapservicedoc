import os
import sys
import re
import json
import datetime
import requests
from tqdm import tqdm
from ast import literal_eval

def log(message):
    refreshLog = os.path.join(os.getcwd(), "serviceAggProc.log")
    with open(refreshLog, 'a') as logMessage:
        logMessage.write('%s - %s\n' % (str(datetime.datetime.now()), str(message)))    
    return


def getJsonData(url):
    responce = requests.get(url)
    
    if responce.status_code > 206:
        raise Exception('Application did not handle import success message properly for',url)
    
    dataDict = json.loads(json.dumps(responce.json()))
    
    if 'error' in dataDict:
        return 'error'
    else:
        return dataDict


def itosMapServises():

    log("Accessing list of services...")
    # App log
    COD_External_URL = 'https://gistmaps.itos.uga.edu/arcgis/rest/services/COD_External/?f=pjson'

    codExternalDataDict = getJsonData(COD_External_URL)
    
    jsonData = []
    codCountry = [countryData for countryData in codExternalDataDict['services'] if countryData['name'].endswith('pcode')]
    
    for codData in tqdm(codCountry,desc='Services'):
        
        codCountry_url = 'https://gistmaps.itos.uga.edu/arcgis/rest/services/'+codData["name"]+'/FeatureServer/?f=pjson'
        #print(codCountry_url)
        adminAcessList = ['Admin0', 'Admin1', 'Admin2', 'Admin3',]

        countryDataDict = json.loads(json.dumps(getJsonData(codCountry_url)))

        dataDict = 'test'
        
        for layer in countryDataDict['layers']:
            if layer['name'] in adminAcessList:
                admin = layer['name'].lower()
#                 adminURL = 'https://gistmaps.itos.uga.edu/arcgis/rest/services/'+codData["name"]+'/MapServer/'+str(layer['id'])+'/query?where=0%3D0&outFields=*&f=pjson'
                adminURL = 'https://gistmaps.itos.uga.edu/arcgis/rest/services/'+codData["name"]+'/FeatureServer/'+str(layer['id'])+'/query?where=0%3D0&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields=*&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=&gdbVersion=&historicMoment=&returnDistinctValues=false&returnIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&multipatchOption=&resultOffset=&resultRecordCount=&returnTrueCurves=false&sqlFormat=none&f=geojson'
                print (adminURL)
                datadict = adminURL + ', '  + dataDict


    #jsonData = list({i['country']:i for i in jsonData}.values())   
    jsonData = dataDict            
    return jsonData

def addLanguageCode(metaData):
    languageCodes = requests.get('https://datahub.io/core/language-codes/r/language-codes.json').json()
    languageDict = {}
    for langDict in languageCodes:
        alpha2 = langDict['alpha2']
        language = langDict['English']
        languageDict[alpha2] = language
        
    for metaDict in metaData:
        adminName = [key for key,value in metaDict.items() if key.startswith('admin0Name') and len(key)==(len('admin0Name')+3)]
        if adminName:
            metaDict['languageCode'] = {}
            for admin0 in adminName:
                alpha2 = admin0[-2:]
                if alpha2 in languageDict:
                    metaDict['languageCode'].update({alpha2:languageDict[alpha2]})
                else:
                    metaDict['languageCode'].update({alpha2:'unknown'})
                
    return metaData


def getCODData(fileName):
    
    log("Beginning python process...")
    
    metaData = itosMapServises()
    
    print('Adding language code to the retrived ITOS data.')
    
    #metaData = addLanguageCode(metaData)
    
    with open(fileName,'w') as fp:
        json.dump(metaData, fp, indent=4)
    print('Data has written into %s file' %(fileName))
    log("Python process complete...")

    
def main(fileName):
    print("Enter the JSON filename or filepath:")
    fileName = str(input())
    
    getCODData(fileName)
    
    print("Process Compelete.")
    
    
main('v00.json')
