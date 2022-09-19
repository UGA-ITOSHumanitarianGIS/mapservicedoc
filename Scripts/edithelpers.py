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
path_of_the_directory= r"c:\\Users\arusso.os\Documents\GitHub\mapservicedoc\scripts\CountryModels_PopStats"

origHelper = os.path.join(path_of_the_directory, "BGDHandler.cs")

with open(helpers) as cod_file:
    for line in cod_file:
        if (len(line)> 0):
            cc = line[4:7]
            cod = cc + "Handler.cs"
            repTxt1 = "BGDPopStats"
            entity = "bgd_admpop_adm3_bd"
            print(os.path.join(path_of_the_directory, cod))
            edFile = open(os.path.join(path_of_the_directory, cod), mode='r')
            helper_file = edFile.readlines();
            edFile.close()
            j = open(os.path.join(path_of_the_directory, cod), mode='w')
            for edline in helper_file:
                if (re.match(".*AppSettings*", edline) != None):
                    edline = edline.replace(repTxt1, cc.upper() + "PopStats")
                    #helper_file.write(edline)
                if (re.match(".*" + entity + "*", edline) != None):
                    edline = edline.replace(entity, line.strip())
                    #helper_file.write(edline)
                if (re.match(".*class bgd*", edline) != None):
                    edline = edline.replace("bgd", cc)
                if (re.match(".*public bgd*", edline) != None):
                    edline = edline.replace("bgd", cc)
                j.write(edline)
            j.close()
                        
                        
                
##            if (cod != "bgdHandler.cs"):
##                newfile = os.path.join(path_of_the_directory, cod)
##                print(origHelper + ", " + newfile)
##                shutil.copy(origHelper, newfile)
        
        #print (line,)  # The comma to suppress the extra new line char
#####
##path_of_the_directory= r"\\os.uga.edu\onu-ocha\team_files\deliverables\2019-2022WorkPlan\COD\PopulationStatistics\hdxData"
##print("Files and directories in a specified path:")
##for filename in os.listdir(path_of_the_directory):
##    f = os.path.join(path_of_the_directory,filename)
##    if os.path.isfile(f):
##        print(f)
##    else:
##        y = os.listdir(f)
##        for fn in y:
##            f2 = os.path.join(f,fn)
##            print(f2)
##            cod = fn[0:3]
##            yr = fn[len(fn) - 8:len(fn) - 4]
##            #log(cod + ", " + yr + "\n")
##            #os.system('cmd /k "csvsql "' + f2)
##            #subprocess.run(["csvsql ", f2 + " >> file.txt"])
##            #o = open('createstmt.sql', 'a')
##            #subprocess.call(["csvsql ", f2], stdout=o)
#####
