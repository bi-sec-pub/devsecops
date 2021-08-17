import os
import argparse
import xml.etree.ElementTree as ET
from datetime import datetime, date
import time
import csv

args = argparse.ArgumentParser()
args.add_argument("--filepath", "-f", default=False, help="filepath", required=True)
args.add_argument("--exceptioncsv", "-e", default=False, help="filepath", required=False)
currArgs = args.parse_args()

filepath = currArgs.filepath
exceptioncsv = currArgs.exceptioncsv

kind_array = []

if os.path.isfile(exceptioncsv):
    with open(exceptioncsv, 'r') as input_file:
        reader = csv.DictReader(input_file, fieldnames=['id', 'exception', 'risk'], delimiter=';', quotechar='"')
        cnt = 0
        for row in reader:
            try:
                if cnt > 0: 
                    kind_array.append(row['id'])
                cnt = cnt +1 
            except TypeError as e:
                print(f"Error: TypeError csv-kind_array.append {e}")

maxCountAlert = 20
countAlert = 0

try:
    modification_time = os.path.getmtime(filepath)
    while modification_time > time.time()-30:
        time.sleep(10)
    local_time = time.ctime(modification_time)
except OSError:
    print ("error")
    exit(-1)

os.system("/usr/bin/pkill perl")

if os.path.isfile(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    #print root

    for item in root.findall('./niktoscan/scandetails/item'):
        skipped = 0
        for val in kind_array:
            if str(item.attrib).find(val) > 0:
                skipped = 1
        if skipped == 0:
                print (item.attrib)
                print (item.find("description").text)
                print (item.find("namelink").text)
                print (item.find("uri").text)
                countAlert +=1
                print ("_________________")

print ("_________________________")
print ("Summary: ")
print ("_________________________")
print ("countAlert: %d" %countAlert)
if countAlert > maxCountAlert:
    print ("Recommendation: abort")
exit()


# Requires CSV file with form id;exception;risk
