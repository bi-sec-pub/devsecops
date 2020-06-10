# Autor: bi-sec GmbH, Christian Biehler
# Content
# _ Sample scriptlet to run sslyze via python

import os
import argparse

args = argparse.ArgumentParser()
args.add_argument("--serverURL", "-s", default=False, help="serverURL", required=True)
currArgs = args.parse_args()

serverURL = currArgs.serverURL
serverURL = serverURL.replace("http://", "")
serverURL = serverURL.replace("https://", "")
serverURL = serverURL.replace("/", "")

executablePath = "/usr/local/bin/sslyze"
executionCommand = "--regular"
outputCommand = "--xml_out="
outFilePath = "./"

os.system(executablePath + " " + executionCommand + " " + serverURL + " " + outputCommand + "" + outFilePath + "/" + serverURL +".xml &")
