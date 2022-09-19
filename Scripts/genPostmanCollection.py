import os
import csvkit
import subprocess
import os
import re
import sys
import traceback
import collections
import shutil

def log(message):
    refreshLog = os.path.join(os.getcwd(), "popstater.log")
    with open(refreshLog, 'a') as logMessage:
        #logMessage.write('%s - %s\n' % (str(datetime.datetime.now()), str(message)))
        logMessage.write(str(message))
    return
helpers = os.path.join(os.getcwd(), "cpsfiles.txt")
scratch = os.path.join(os.getcwd(), "popstatstestPM.txt")
path_of_the_directory= r"c:\\Users\arusso.os\Documents\GitHub\mapservicedoc\scripts\CountryModels_PopStats"

with open(helpers) as cod_file:
    for line in cod_file:
        if (len(line)> 0):
            cc = line[4:7]
            lvl = "9"
            a = re.match(".*adm*\d", line)
            if a!=None:
                if lvl!=None:
                    lvl = re.findall("\d+", a[0])[0]
                else:
                    lvl = 9
            i = 0
            while i<=int(lvl):       
                btext = "https://beta.itos.uga.edu/CODV2API/api/v1/themes/cod-ps/lookup/Get/" + str(i) + "/aa/" + cc
                btext1 = "\n{\n  \"name\": \"" + btext + "\","
                btext2 = "\n  \"request\": {\n    \"method\": \"GET\", \n    \"header\": [],"
                btext3 = "\n    \"url\": {"
                btext4 = "\n       \"raw\": \"" + btext + "\","
                btext5 = "\n       \"protocol\":  \"https\","
                btext6 = "\n       \"host\": ["
                btext7 = "\n           \"beta\","
                btext8 = "\n           \"itos\","
                btext9 = "\n           \"uga\","
                btext10 = "\n           \"edu\","
                btext11 = "\n       ],"
                btext12 = "\n       \"path\": ["
                btext13 = "\n           \"CODV2API\","
                btext14 = "\n           \"api\","
                btext15 = "\n           \"v1\","
                btext16 = "\n           \"themes\","
                btext17 = "\n           \"cod-ps\","
                btext18 = "\n           \"lookup\","
                btext19 = "\n           \"Get\","
                btext20 = "\n           \"" + str(i) + "\","
                btext21 = "\n           \"aa\","
                btext22 = "\n           \"" + cc + "\""
                btext23 = "\n       ]"
                btext24 = "\n      }"
                btext25 = "\n    },"
                btext26 = "\n   \"response\": []"
                btext27 = "\n},"
                
                edFile = open(scratch, mode='a')
                edFile.write(btext1);
                edFile.write(btext2);
                edFile.write(btext3);
                edFile.write(btext4);
                edFile.write(btext5);
                edFile.write(btext6);
                edFile.write(btext7);
                edFile.write(btext8);
                edFile.write(btext9);
                edFile.write(btext10);
                edFile.write(btext11);
                edFile.write(btext12);
                edFile.write(btext13);
                edFile.write(btext14);
                edFile.write(btext15);
                edFile.write(btext16);
                edFile.write(btext17);
                edFile.write(btext18);
                edFile.write(btext19);
                edFile.write(btext20);
                edFile.write(btext21);
                edFile.write(btext22);
                edFile.write(btext23);
                edFile.write(btext24);
                edFile.write(btext25);
                edFile.write(btext26);
                edFile.write(btext27);
                
                edFile.close()
                i += 1        
  
