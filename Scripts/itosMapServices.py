import os
import sys
import re
import json
import datetime
import requests
from tqdm import tqdm


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
    codCountry = [countryData for countryData in codExternalDataDict['services'] if not countryData['name'].endswith('pcode')]
    
    for codData in tqdm(codCountry,desc='Services'):
        
        codCountry_url = 'https://gistmaps.itos.uga.edu/arcgis/rest/services/'+codData["name"]+'/MapServer/query?where=0%3D0&outFields=*&f=pjson'
        
        adminAcessList = ['Admin0', 'Admin1', 'Admin2', 'Admin3',]

        countryDataDict = getJsonData(codCountry_url)

        dataDict = {}

        for layer in countryDataDict['layers']:
            if layer['name'] in adminAcessList:
                admin = layer['name'].lower()
#                 adminURL = 'https://gistmaps.itos.uga.edu/arcgis/rest/services/'+codData["name"]+'/MapServer/'+str(layer['id'])+'/query?where=0%3D0&outFields=*&f=pjson'
                adminURL = 'https://gistmaps.itos.uga.edu/arcgis/rest/services/'+codData["name"]+'/MapServer/'+str(layer['id'])+'/query?where=0%3D0&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=false&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentsOnly=false&datumTransformation=&parameterValues=&rangeValues=&f=pjson'

                adminData = getJsonData(adminURL)

                if adminData == 'error':
                    dataDict[admin] = "Error performing query operation."
                else:
                    adminFetAttribute = adminData['features'][0]['attributes']
                    adminNameList = [(key, value) for key, value in adminFetAttribute.items() if key.startswith(admin+'Name')]

                    for adminName in adminNameList:
                        if adminName[0].endswith('en'):
                            if adminName[0].startswith('admin0'):
                                dataDict['country'] = adminName[1]
                            dataDict[adminName[0]] = adminName[1]
                        else:
                            if adminName[0].startswith('admin0') and 'country' not in dataDict:
                                dataDict['country'] = adminName[1]
                            dataDict[adminName[0]] = adminName[1]
                            dataDict[adminName[0]+'_utf8'] = str(adminName[1].encode())

                    dataDict[admin+'Pcode'] = adminFetAttribute[admin+'Pcode']
                    dataDict[admin+'_url'] = adminURL

                    jsonData.append(dataDict)

    jsonData = list({i['country']:i for i in jsonData}.values())   
                
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
    
    metaData = addLanguageCode(metaData)
    
    with open(fileName,'w') as fp:
        json.dump(metaData, fp, indent=4)
    print('Data has written into %s file' %(fileName))
    log("Python process complete...")

    
def main():
    print("Enter the JSON filename or filepath:")
    fileName = str(input())
    
    getCODData(fileName)
    
    print("Process Compelete.")
    
    
if __name__ == "__main__":
    main()