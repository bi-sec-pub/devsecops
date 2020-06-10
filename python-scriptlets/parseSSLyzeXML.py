# Autor: bi-sec GmbH, Christian Biehler
# Content
# _ Sample scriptlet to parse and evaluate sslyze-xml results
# _ Contains only basic examples

import os
import argparse
import xml.etree.ElementTree as ET

args = argparse.ArgumentParser()
args.add_argument("--filepath", "-f", default=False, help="filepath", required=True)
currArgs = args.parse_args()

filepath = currArgs.filepath
countWarning = 0
countShowStopper = 0
maxWarnings = 3
maxShowStopper = 1
if os.path.isfile(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    # print root

    for child in root:
        pass
        # print(child.tag, child.attrib)

    for elem in root.iter():
        pass
        if (elem.tag.startswith("tls") or elem.tag.startswith("sslv")):  # List protocols supported
            print (elem.attrib)
            if (str(elem.attrib).find("TLSV1 ") > 0 and str(elem.attrib).find("True") > 0):
                print "Warning: WEAK Protocol version"
                countWarning += 1
            if (str(elem.attrib).find("SSLV") > 0 and str(elem.attrib).find("True") > 0):
                print "ShowStopper: WEAK Protocol version"
                countShowStopper += 1

    # List of TLSv1.2 Cipher suites
    print "### GET TLS1_2 Cipher Suites ###"
    for cipher in root.findall('./results/target/tlsv1_2/acceptedCipherSuites/cipherSuite'):
        print(cipher.attrib)  # , cipher.text
        if (str(cipher.attrib).find("CBC") > 0):
            print "Warning: WEAK CBC-Cipher"
            countWarning += 1

print "_________________________"
print "Summary: "
print "Warnings: " + str(countWarning) + "/" + str(maxWarnings)
if countWarning > maxWarnings:
    print "Recommendation: abort"
print "Showstopper: " + str(countShowStopper) + "/" + str(maxShowStopper)
if countShowStopper > maxShowStopper:
    print "Recommendation: abort"
print "_________________________"
