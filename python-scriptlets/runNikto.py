import os
import argparse

args = argparse.ArgumentParser()
args.add_argument("--serverURL", "-s", default=False, help="serverURL", required=True)
currArgs = args.parse_args()

serverURL = currArgs.serverURL
filePath = serverURL.replace("http://", "")
filePath = filePath.replace("https://", "")
filePath = filePath.replace("/", "")

executablePath = "/usr/bin/perl /usr/bin/nikto"
executionCommand = "-host"
outputCommand = "-output"
fileformatCommand = "-Format XML"
outFilePath = "/root/nikto/"

os.system(executablePath + " " + executionCommand + " " + serverURL + " " + fileformatCommand + " " + outputCommand + " " + outFilePath + "results_nikto_" + filePath +".xml &")
exit()
