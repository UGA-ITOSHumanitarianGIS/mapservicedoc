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

def fileValidation(fileName, tags):
    '''
    Helper function for getData() [fileName or filePath].
    '''
    if fileName is None:
        fileName = ''.join([tags,'.json'])
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

def getData(tags, themeList, fileName = None):
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

    fileName => (optional) If not given than the tags string will be taken as fileName
                fileName can be a filePath also with the fileName.

    Return:
    Saves a json format of the filtered tag Datasets.
    '''
    
    tagDatasets = dataLookup(tags)
    
    fileName = fileValidation(fileName, tags)
    
    jsonData = []
    
    for dataset in tagDatasets:
        theme = getTheme(themeList,dataset)
        
        try:
            dueDate = dataset['due_date']
        except:
            dueDate =  None
        
        dataDict = {'title': dataset['title'],
                    'id': dataset['id'],
                    'theme': theme,
                    'tags': dataset.get_tags(),
                    'country': json.loads(dataset['solr_additions'])['countries'],
                    'organization': dataset['organization']['title'],
                    'datasetDate': dataset['dataset_date'],
                    'updateFrequency':dataset['data_update_frequency'],
                    'dueDate': dueDate,
                    'format':{}
        }
        resources = Dataset.get_all_resources([dataset])
        
        for res in resources:
            restype = {res['format']:{'resoource_id':res['id'],
                                      'download_url':res['download_url'],
                                      'description':res['description']
                                     }
            }
            dataDict['format'].update(restype)
        
        jsonData.append(dataDict)
        
        with open(fileName, 'w') as fp:
            json.dump(jsonData, fp, indent=4)
            
    print('Data has written into %s file' %(fileName))