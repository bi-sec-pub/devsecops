# Autor: bi-sec GmbH, Christian Biehler
# Content
# _ Sample scriptlet to parse and evaluate owaspZap JSON results
# _ Contains only basic examples
import json
import argparse
import os
import ast

args = argparse.ArgumentParser()
args.add_argument("--filepath", "-f", default=False, help="filepath", required=True)
currArgs = args.parse_args()
countCritical = 0
countHigh = 0
countMedium = 0
countLow = 0
countInformational = 0

# Define max values
maxCrit = 1
maxHigh = 2
maxMedium = 9999
maxLow = 9999

filepath = currArgs.filepath

if os.path.isfile(filepath):
    currFile = open(filepath, 'r')
    fileContent = currFile.read()
    data_dict = ast.literal_eval(fileContent)  # solves single-quote issue with json.loads
    jsonDump = json.dumps(data_dict)
    jsonContent = json.loads(jsonDump)
    countAlert = 0
    for entry in jsonContent:
        if entry["risk"].find("Critical") > -1:
            print "Alarm: " + entry["alert"]
            print "URL: " + entry["url"]
            print "Param: " + entry["param"]
            print "Attack: " + entry["attack"]
            print "_____"
            pass
            countCritical += 1
        if entry["risk"].find("High") > -1:
            print "Alarm: " + entry["alert"]
            print "URL: " + entry["url"]
            print "Param: " + entry["param"]
            print "Attack: " + entry["attack"]
            print "_____"
            pass
            countHigh += 1
        if entry["risk"].find("Medium") > -1:
            print "Alarm: " + entry["alert"]
            print "URL: " + entry["url"]
            print "Param: " + entry["param"]
            print "Attack: " + entry["attack"]
            print "_____"
            pass
            countMedium += 1
        if entry["risk"].find("Low") > -1:
            pass
            countLow += 1
        if entry["risk"].find("Informational") > -1:
            pass
            countInformational += 1
        countAlert += 1
    print "Number of Alerts: " + str(countAlert)
    print "_____"
    print "#### Summary of Findings ####"
    print "Critical: " + str(countCritical)
    print "High: " + str(countHigh)
    print "Medium: " + str(countMedium)
    print "Low: " + str(countLow)
    print "Informational: " + str(countInformational)

    if countCritical + countHigh + countMedium + countLow + countInformational < countAlert:
        print "WARNING: Something went wrong counting and categorizing Alert criticality."
    if countCritical > maxCrit or countHigh > maxHigh or countMedium > maxMedium or countLow > maxLow:
        print "Recommendation: abort"

