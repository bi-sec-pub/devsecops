# Autor: bi-sec GmbH, Christian Biehler
# Content
# _ Sample scriptlet to parse and evaluate sslyze-JSON results
# _ Contains only basic examples

import os
import argparse
import json

args = argparse.ArgumentParser()
args.add_argument("--filepath", "-f", default=False, help="filepath", required=True)
currArgs = args.parse_args()

filepath = currArgs.filepath
countWarning = 0
countShowStopper = 0
maxWarnings = 3
maxShowStopper = 1
if os.path.isfile(filepath):
    currFile = open(filepath, 'r')
    fileContent = currFile.read()
    jsonContent = json.loads(fileContent)

    for entry in jsonContent['server_scan_results']:
        for sub in entry['scan_commands_results']['ssl_2_0_cipher_suites']['accepted_cipher_suites']:
                print("__SSL2.0__")
                print(sub['cipher_suite']['name'])
                print("ShowStopper: WEAK Protocol version")
                countShowStopper += 1
        for sub in entry['scan_commands_results']['ssl_3_0_cipher_suites']['accepted_cipher_suites']:
                print("__SSL3.0__")
                print(sub['cipher_suite']['name'])
                print("ShowStopper: WEAK Protocol version")
                countShowStopper += 1
        for sub in entry['scan_commands_results']['tls_1_0_cipher_suites']['accepted_cipher_suites']:
                print("__TLS1.0__")
                print(sub['cipher_suite']['name'])
                if sub['cipher_suite']['name'].find('CBC') > 0:
                        print("Warning: WEAK CBC-Cipher")
                        countWarning += 1
        for sub in entry['scan_commands_results']['tls_1_1_cipher_suites']['accepted_cipher_suites']:
                print("__TLS1.1__")
                print(sub['cipher_suite']['name'])
                if sub['cipher_suite']['name'].find('CBC') > 0:
                        print("Warning: WEAK CBC-Cipher")
                        countWarning += 1
        for sub in entry['scan_commands_results']['tls_1_2_cipher_suites']['accepted_cipher_suites']:
                print("__TLS1.2.__")
                print(sub['cipher_suite']['name'])
                if sub['cipher_suite']['name'].find('CBC') > 0:
                        print("Warning: WEAK CBC-Cipher")
                        countWarning += 1
        for sub in entry['scan_commands_results']['tls_1_3_cipher_suites']['accepted_cipher_suites']:
                print("__TLS1.3__")
                print(sub['cipher_suite']['name'])
                if sub['cipher_suite']['name'].find('CBC') > 0:
                        print("Warning: WEAK CBC-Cipher")
                        countWarning += 1

        pass

print("_________________________")
print("Summary: ")
print("Warnings: " + str(countWarning) + "/" + str(maxWarnings))
if countWarning > maxWarnings:
    print("Recommendation: abort")
print("Showstopper: " + str(countShowStopper) + "/" + str(maxShowStopper))
if countShowStopper > maxShowStopper:
    print("Recommendation: abort")
print("_________________________")
