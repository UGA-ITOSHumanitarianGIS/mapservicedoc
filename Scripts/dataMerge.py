import os
import json

def getJSONData(filePath):
    
    with open(filePath, 'r') as fp:
        jsonData = json.load(fp)
        
    return jsonData


def getCleanData(dataList):
    
    cleanData = []
    for data in dataList:
        if data['theme'] != 'unknown':
            cleanData.append(data)
            
    return dataList


def mergeCOD(hdxPath, itosPath, destination):
    
    print("Initiating cleaning for HDX data, based on themes")
    hdxData = getCleanData(getJSONData(hdxPath))
    print("Number of CODs in HDX: %d"%(len(hdxData)))
    itosData = getJSONData(itosPath)
    print("Number of CODs in ITOS: %d"%(len(itosData)))
    
    for hdxCOD in hdxData:
        for itosCOD in itosData:
            if itosCOD['country'] in hdxCOD['country']:
                hdxCOD.update(itosCOD)
                
                
    with open(destination,'w') as fp:
        json.dump(hdxData, fp, indent=4)
        
    print("Process Compelete, Data has been written into %s"%(destination))
        
        
def main():
    print("Enter the HDX data json file path:")
    hdxPath = str(input())
    print("")
    print("Enter the ITOS data json file path:")
    itosPath = str(input())
    print("")
    print("Enter the destination with filename:")
    destPath = str(input())
    print("")
    
    mergeCOD(hdxPath, itosPath, destPath)
    
    
if __name__ == '__main__':
    main()
    
    