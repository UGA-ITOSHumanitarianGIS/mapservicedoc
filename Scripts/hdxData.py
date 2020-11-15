import json
from os import path
import numpy as np
from hdx.utilities.easy_logging import setup_logging
from hdx.hdx_configuration import Configuration
from hdx.data.dataset import Dataset

setup_logging()

Configuration.create(hdx_site='prod', user_agent='getData', hdx_read_only=True)

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
    print("%d number of Resources found" %(len(resources)))
    
    return tagDatasets

def fileValidation(fileName = None):
    '''
    Helper function for getData() [fileName or filePath].
    '''
    if fileName is None:
        fileName = ''.join(['hdxCODData','.json'])
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
    
    tagDatasets = dataLookup(tags)
    
    jsonData = []
    
    for dataset in tagDatasets:
        theme = getTheme(themeList,dataset)
        
        keyCheck = ['due_date','caveats','license_other','methodology_other']
        for key in keyCheck:
            if key not in dataset:
                dataset[key] = None
        
        isoCodes = getISOCode(dataset['groups'])
        
        dataDict = {'title': dataset['title'],
                    'id': dataset['id'],
                    'theme': theme,
                    'datasetDescription': dataset['notes'],
                    'caveats': dataset['caveats'],
                    'tags': dataset.get_tags(),
                    'iso': isoCodes,
                    'location': json.loads(dataset['solr_additions'])['countries'],
                    'datasetSource': dataset['dataset_source'],
                    'organization': dataset['organization']['title'],
                    'datasetDate': dataset['dataset_date'],
                    'updateFrequency':dataset['data_update_frequency'],
                    'dueDate': dataset['due_date'],
                    'license_id': dataset['license_id'],
                    'license_other':dataset['license_other'],
                    'license_title':dataset['license_title'],
                    'methodology': dataset['methodology'],
                    'methodology_other': dataset['methodology_other'],
                    'format':{}
        }
        resources = Dataset.get_all_resources([dataset])
        
        for res in resources:
            restype = {res['format']:{'resource_id':res['id'],
                                      'created':res['created'],
                                      'last_modified':res['last_modified'],
                                      'revision_last_updated':res['revision_last_updated'],
                                      'download_url':res['download_url'],
                                      'description':res['description']
                                     }
            }
            dataDict['format'].update(restype)
        
        jsonData.append(dataDict)
        
    return jsonData

def saveJSON(codData, fileName):
    '''
    Helper function for storing COD Metadata in a JSON format
    
    Parameters:
    COD Metadata (List) => It can fetch from getCODData function
    
    fileName (String) => fileValidation function will return the fileName
    
    Returns: Saves a JSON file with COD Metadata
    '''
    with open(fileName, 'w') as fp:
        json.dump(codData, fp, indent=4)
            
    print('Data has written into %s file' %(fileName))
    
    
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
    saveJSON(codData, fileName)