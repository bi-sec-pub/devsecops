# Autor: bi-sec GmbH, Christian Biehler
# Content
# _ Sample scriptlet to run OWASPzap via zapv2
# _ Contains only the basic examples from the api specs
import time
from pprint import pprint
from zapv2 import ZAPv2
import argparse

# The URL of the application to be tested
args = argparse.ArgumentParser()
args.add_argument("--serverURL", "-s", default=False, help="serverURL", required=True)
currArgs = args.parse_args()

target = currArgs.serverURL
# Change to match the API key set in ZAP, or use None if the API key is disabled
apiKey = 'lknfoui83z4uwlrg3l'
zapServerAPI = '127.0.0.1:8080'
zap = ZAPv2(apikey=apiKey, proxies={'http': 'http://' + zapServerAPI, 'https': 'http://' + zapServerAPI})

print('Spidering target {}'.format(target))
# The scan returns a scan id to support concurrent scanning
scanID = zap.spider.scan(target)
try:
    while int(zap.spider.status(scanID)) < 100:
        # Poll the status until it completes
        print('Spider progress %: {}'.format(zap.spider.status(scanID)))
        time.sleep(1)
except ValueError as e:
    print (e)
print('Spider has completed!')
# Prints the URLs the spider has crawled
print('\n'.join(map(str, zap.spider.results(scanID))))
# If required post process the spider results

## AJAX Spider
print('Ajax Spider target {}'.format(target))
scanID = zap.ajaxSpider.scan(target)

timeout = time.time() + 60   # 1 minute from now
# Loop until the ajax spider has finished or the timeout has exceeded
while zap.ajaxSpider.status == 'running':
    if time.time() > timeout:
        break
    print('Ajax Spider status' + zap.ajaxSpider.status)
    time.sleep(10)

print('Ajax Spider completed')
ajaxResults = zap.ajaxSpider.results(start=0, count=10)

## Passive Scan
while int(zap.pscan.records_to_scan) > 0:
    # Loop until the ajax spider has finished or the timeout has exceeded
    print('Records to passive scan : ' + zap.pscan.records_to_scan)
    time.sleep(2)

print('Passive Scan completed')

# Print Passive scan results/alerts
print('Hosts: {}'.format(', '.join(zap.core.hosts)))
print('Alerts: ')
newFileRunning = open("results_ZapPassiveScan.json", "w")
newFileRunning.write(str(zap.core.alerts()))
newFileRunning.close()
pprint(zap.core.alerts())

## Active scan

print('Active Scanning target {}'.format(target))
scanID = zap.ascan.scan(target)
while int(zap.ascan.status(scanID)) < 100:
    # Loop until the scanner has finished
    print('Scan progress %: {}'.format(zap.ascan.status(scanID)))
    time.sleep(60)

print('Active Scan completed')
# Print vulnerabilities found by the scanning
print('Hosts: {}'.format(', '.join(zap.core.hosts)))
print('Alerts: ')
newFileRunning = open("results_ZapActiveScan.json", "w")
newFileRunning.write(str(zap.core.alerts()))
newFileRunning.close()
pprint(zap.core.alerts(baseurl=target))
