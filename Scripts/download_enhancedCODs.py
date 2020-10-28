import os
import wget
import json
from tqdm import tqdm
import multiprocessing as mp
from multiprocessing import Pool

def createDestination(path):
    try:
        os.makedirs(path)
    except:
        pass

def downloadCODs(codMeta, destination = None):
    
    if destination == None:
        destination = os.path.join(os.getcwd(),'hdxData/')
        
    iso = codMeta['iso'][0]
    codCountry = ''.join(['COD_',iso.upper()])
    title = codMeta['title']
    formatDict = codMeta['format']
    for formatType in formatDict:
        if formatType != 'LIVE SERVICE':
            path = os.path.join(destination,formatType,codCountry,title)
            createDestination(path)
            url = formatDict[formatType]['download_url']
            fileName = os.path.basename(url)
            outFile = os.path.join(path,fileName)
            try:
                wget.download(url,outFile)
            except:
                print('Error 404:',url)
                print('Destination:',path)
                
def main(enhancedCODPath, destination=None):
    
    with open(enhancedCODPath,'r') as fp:
        codData = json.load(fp)
    
    core = mp.cpu_count()
    with Pool(core) as p:
        r = list(tqdm(p.imap(downloadCODs,codData),total = len(codData)))