import json
import os
from os import path
import numpy as np
from hdx.utilities.easy_logging import setup_logging
from hdx.api.configuration import Configuration
from hdx.data.dataset import Dataset
import re
from itertools import chain
import requests


setup_logging()

Configuration.create(hdx_site='prod', user_agent='getData', hdx_read_only=True)
masterL = []

def dataLookup(tags):
    '''
    dataLookup is used to search and filter the desired datasets using Humanitarian Data Exchange API.
    It can take multiple tags as a query and look through the HDX datasets.
    
    Helper function for getData()
    
    Parametes:
    
    tags => dataType -> string
            For multiple tag filters, give it in a single string sperated by comma(,)
            I.e. tags = 'common operational dataset - cod,administrative divisions'
    
    Returns:
    It returns a list of filtered tag Datasets.
    '''
    tagList = tags.split(',')
    datasets = Dataset.search_in_hdx(tagList[0])
    #datasets = Dataset.search_in_hdx("Subnational Administrative Boundaries")
    #print(tagList[0])
    tagDatasets = []
    for data in datasets:
        
        check = []
        for tag in tagList:
            if tag in data.get_tags():
                check.append(True)
            else:
                check.append(False)
        
        if np.array(check).all() == True:
            tagDatasets.append(data)
    
    print("%d number of %s datasets found" %(len(tagDatasets),tags))
    
    resources = Dataset.get_all_resources(tagDatasets)
    '''for res in resources:
        print (res)
        restype = {res['format']:{'resource_id':res['id'],
        'resource_name':res['name'],
        'created':res['created'],
        'last_modified':res['last_modified'],
                                          #'revision_last_updated':res['revision_last_updated'],
        'download_url':res['download_url'],
        'description':res['description']
        }
    }
    '''
    print("%d number of Resources found" %(len(resources)))
    
    return tagDatasets

def fileValidation(fileName = None):
    '''
    Helper function for getData() [fileName or filePath].
    '''
    if fileName is None:
        fileName = ''.join(['hdxCODDataName','.json'])
    else:
        if fileName.endswith('.json'):
            pass
        else:
            fileName = ''.join([fileName,'.json'])
    
    if path.exists(fileName) == True:
        print('%s file already exists. Want to overwrite the data in the same file(yes/no)?' %(fileName))
        userInput = str(input())
        
        if userInput.lower() == 'yes':
            pass
        elif userInput.lower() == 'no':
            print('Enter the file name, if destination is different than current working directory than enter the file path with the file name.')
            userFileInput = str(input())
            if userFileInput.endswith('.json'):
                fileName = userFileInput
            else:
                fileName = ''.join([userFileInput,'.json'])
        else:
            print('Invalid Answer')
    
    return fileName

def getTheme(themeList,dataset):
    """
    Helper function for parsing themes in the title
    :param themeList: List of themes want to get.
    :param dataset: hDX dataset where themes are going to parse.
    :return: appropriate theme (string), if theme not found in dataset than 'unknown' is return.
    """

    title = dataset['title'].lower()

    for themeType in themeList:
        themeType = themeType.lower()
        if (themeType in title) or (themeType.split()[0] in title) or (themeType.split()[-1] in title):
            theme = themeType
            break
        else:
            theme = 'unknown'
    
    return theme

def getISOCode(groupList):
    """
    Helper function for getting ISO code for countaries from dataset
    
    Parameters:
    groupList (List) => Groups presesnt in the hDX datasets.
    
    Returns: List of iso code associated to the countries from hDX datasets.
    """
    isoCodes = []
    for groupMember in groupList:
        isoCodes.append(groupMember['id'])
    
    return isoCodes


def getCODData(tags, themeList):
    '''
    getData takes two arguments tags and fileName/filePath to save json file.
    If multiple tags are presents for a query than give a single string of tags separated by comma(,).

    Parameters:

    tags => dataType -> string
            For multiple tag filters, give it in a single string separated by comma(,)
            I.e. tags = 'common operational dataset - cod,administrative divisions'

    themeList => dataType -> List of Strings
                 For different themes in the datasets
                 I.e. themeList = ['administrative boundaries','population statistics']

    Return:
    COD Metadata => dataType -> List of Dictionary 
    '''

    #Create iso and resource list
    
    tagDatasets = dataLookup(tags)
    
    jsonData = []
    for dataset in tagDatasets:
        theme = getTheme(themeList,dataset)
        
        keyCheck = ['due_date','caveats','license_other','methodology_other','contributor']
        for key in keyCheck:
            if key not in dataset:
                dataset[key] = None
        
        isoCodes = getISOCode(dataset['groups'])
        title = dataset['title'].lower()
        
        if (title.__contains__('subnational population statistics')):
            if dataset['is_requestdata_type']:
                dataDict = {'title': dataset['title'],
                        'id': dataset['id'],
                        'iso': isoCodes,
                        'location': json.loads(dataset['solr_additions'])['countries'],
                        'format':{}
                }
            else:
                dataDict = {'title': dataset['title'],
                        'id': dataset['id'],
                        'iso': isoCodes,
                        'location': json.loads(dataset['solr_additions'])['countries'],
                        'format':{}
            }
            resources = Dataset.get_all_resources([dataset])
            #resources = dataset.get_resources()
            
            for res in resources:
                # res props:
                #print(res['download_url'])
                restype = {res['id']:{'resource_id':res['id'],
                              'resource_name':res['name'],
                              'created':res['created'],
                              'last_modified':res['last_modified'],
                              #'revision_last_updated':res['revision_last_updated'],
                              'download_url':res['download_url'],
                              'description':res['description'],
                              'format':res['format']
                             }
                }
                dataDict['format'].update(restype)
    
            jsonData.append(dataDict)

    return jsonData

def hilevListr (hilev):
     '''
    Parses the list to remove items if they are not the highest level for the country
    Works based on filename with csv and adm + level number pattern.

    Parameters:

    hilev => dataType -> dictionary
            level and download url

    Return:
    COD Metadata => dataType -> List of Dictionary 
    '''
    x = hilev.keys()
    t = list(x)[0]
    lCheck = list(hilev.values())
    i = 0
    idx = t.rfind('/')
    f = t[idx+1:len(t)]
    for n in masterL:
        ir = None
        idx = n.rfind('/')
        o = n[idx+1:len(n)]
        b = re.match("[\s\S]{0,3}", o)
        c = re.match("[\s\S]{0,3}", f)

        if (b[0] == c[0]):  
            for z in o.split('_'):
                a = re.match(".*adm*\d", z)
                if a!=None:
                    j = re.findall("\d+", a[0])[0]
                    if j != None:
                        if j < lCheck[0]:
                            ir = n;
                        if j > lCheck[0]:
                            ir = t
                        
        i += 1
        if ir != None:
            if ir in masterL:
                masterL.remove(ir)
        
    return lCheck

def downloadList(codData, fileName):
    '''
    Helper function for storing COD Metadata in a JSON format
    
    Parameters:
    COD Metadata (List) => It can fetch from getCODData function
    
    fileName (String) => fileValidation function will return the fileName
    
    Returns: downloads population statistics from HDX
    '''

    ''' parse the jsonfile of datasets and resources so that
        population statistics files with the highest level are downloaded only
    '''
    
    isoMasterList = []
    for j in codData:
    
        for key in j['format']:
            rc = j['format'][key]['download_url']
            #print (rc)
            isoItem = [j['iso'][0], str(rc)]
            isoMasterList.append(isoItem)
            #print (len(isoMasterList))


    for k in isoMasterList: 
        x = re.match(".*adm.*?csv$", k[1])
        if x == None:
            isoMasterList.remove(k)
    
    #for each unique iso get highest level csv

    for n in isoMasterList:
        hilev = None
        #add the file
        idx = n[1].rfind('/')
        o = n[1][idx+1:len(n[1])]
        x = re.match(".*adm.*?csv$", o)
        if x != None:
        #remove the file from the master list if there is already a file with the iso code match and adm + n pattern
            if (o not in masterL):
                masterL.append(n[1])

            for z in o.split('_'):
                    b = re.findall("\d+", x[0])[0]
                    if b != None:
                        hilev = {n[1]: b}
            if hilev != None:            
                r = hilevListr (hilev)

    destination = os.path.join(os.getcwd(),'hdxData')
    for i in masterL:
        idx = i.rfind('/')
        o = i[idx+1:len(i)]
        fpath = o[0:len(o)-4]
        path = os.path.join(destination,fpath)
        createDestination(path)
        fileName = os.path.basename(o)
        outFile = os.path.join(path,o)
        try:
            response = requests.get(i, stream=True)
            open(outFile, "wb").write(response.content)
        except Exception as e:
            print('Error 404:',e)
            print('Destination:',path)    
    #following commented out for downloading instead of serializing the list to a file.
    #with open(fileName, 'w') as fp:
    #    json.dump(masterL, fp, indent=4)
            
    print('Data has been downloaded %s file' %(fileName))

def createDestination(path):
    try:
        os.makedirs(path)
    except:
        pass

def main(tags, themeList, fileName = None):
    '''
    Main Wraper function which takes three arguments tags, themeList and fileName/filePath (optional) to save json file.
    If multiple tags are presents for a query than give a single string of tags separated by comma(,).

    Parameters:

    tags => dataType -> string
            For multiple tag filters, give it in a single string separated by comma(,)
            I.e. tags = 'common operational dataset - cod,administrative divisions'

    themeList => dataType -> List of Strings
                 For different themes in the datasets
                 I.e. themeList = ['administrative boundaries','population statistics']
                 
    fileName (optional) => dataType -> String
                It can be a fileName or the filePath with the fileName

    Return:
    Saves a JSON file with COD Metadata
    '''
    
    codData = getCODData(tags, themeList)
    fileName = fileValidation(fileName)
    downloadList(codData, fileName)

main('common operational dataset - cod', "['population statistics']")
