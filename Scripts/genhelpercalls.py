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
scratch = os.path.join(os.getcwd(), "cpsblock.txt")
path_of_the_directory= r"c:\\Users\arusso.os\Documents\GitHub\mapservicedoc\scripts\CountryModels_PopStats"

with open(helpers) as cod_file:
    for line in cod_file:
        if (len(line)> 0):
            cc = line[4:7]
            btext1 = "if (iso3Rec.ToLower() == \"" + cc + "\")\n"
            btext2 = "{\n"
            btext3 = "\tCODV2API.Handlers.CountryModels_PopStats." + cc + " " + cc+ "Helper = new Handlers.CountryModels_PopStats." + cc + "(iso3Rec, level);\n"
            btext4 = "\tvar o = Json(" + cc + "Helper.popstats(iso3Rec, level));\n"
            btext5 = "\tif ((o.Content is null))\n"
            btext6 = "\t\treturn Content(HttpStatusCode.NotImplemented, \"This result for parameters \" + level + \", \" + iso3Rec + \" is unavailable at this time.\");\n"
            btext7 = "\treturn o;\n"
            btext8 = "}\n"
            edFile = open(scratch, mode='a')
            edFile.write(btext1);
            edFile.write(btext2);
            edFile.write(btext3);
            edFile.write(btext4);
            edFile.write(btext5);
            edFile.write(btext6);
            edFile.write(btext7);
            edFile.write(btext8);
            edFile.close()
                        
                        
                
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
