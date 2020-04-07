# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# CODServiceLookups.py
# Created on: 2020-04-06 09:48:01.00000
#   (generated by ArcGIS/ModelBuilder)
# Author: ADR
# Description: Parse the services hosted by ITOS to get the level data and
#   Hydrate a datasource for CODVersion2 API
# Called by: n/a
# ---------------------------------------------------------------------------

# Import arcpy module
import json
import sys
import datetime
import urllib2
import requests
import os


# Local variables:
 
refreshLog = os.path.join(os.getcwd(), "lookuprefresh.log")#r"c$\\scripts\\USAIDCODV2Process\\lookuprefresh.log"

def log(message):
    with open(refreshLog, 'a') as logMessage:
        logMessage.write('%s - %s\n' % (str(datetime.datetime.now()), str(message)))    
    return

def doRefresh():

    try:
       
        log("Accessing list of services...")

        # App log
        url = 'https://gistmaps.itos.uga.edu/arcgis/rest/services/COD_External/?f=pjson'
        ret = requests.get(url)
		
		
        if ret.status_code > 206:
             raise Exception(' application did not handle import success message properly.')

        obj = ret.json()
        svcs = json.dumps(obj)
        log(svcs)
			
    except Exception, e:
        log("Exception caught:  " + str(e))
        return

    log("data refresh completed!")
    return

# Run app with messaging and flow
log("Beginning python process...")
doRefresh()
log("Python process complete...")
