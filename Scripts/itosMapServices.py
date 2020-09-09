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

    for codData in tqdm(codExternalDataDict['services']):
        if codData['type'] == 'MapServer' and not re.search('pcode',codData['name']):
            codCountry_url = 'https://gistmaps.itos.uga.edu/arcgis/rest/services/'+codData["name"]+'/MapServer/query?where=0%3D0&outFields=*&f=pjson'
            adminAcessList = ['Admin0', 'Admin1', 'Admin2', 'Admin3',]

            countryDataDict = getJsonData(codCountry_url)

            dataDict = {}

            for layer in countryDataDict['layers']:
                if layer['name'] in adminAcessList:
                    admin = layer['name'].lower()
                    adminURL = 'https://gistmaps.itos.uga.edu/arcgis/rest/services/'+codData["name"]+'/MapServer/'+str(layer['id'])+'/query?where=0%3D0&outFields=*&f=pjson'

                    adminData = getJsonData(adminURL)
                    
                    if adminData == 'error':
                        dataDict[admin] = "Error performing query operation."
                    
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

    return jsonData


def getCODData(fileName):
    
    log("Beginning python process...")
    
    metaData = itosMapServises()
    
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