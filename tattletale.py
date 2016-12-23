import urllib.request
import os
import os.path
import platform
import configparser
import time

from tattletaleled import *      # Raspberry Pi on-board LED control
from tattletaledb import *       # SqLite database functions
from tattletalemail import *     # Optional Gmail interface
from tattletaletwitter import *  # Optional Twitter auto-shaming

def isUp(host: str) -> bool:
    pingCmd = r"C:\Windows\System32\PING.EXE -n 1" if platform.system().lower() == "windows" else "ping -c 1"
    return os.system(pingCmd + " " + host + ">NUL") == 0

def grabStatus(momemUrl: str, modemStatusPages: list, logDir: str):
    for statusPage in modemStatusPages:
        url = 'http://{}/{}'.format(modemUrl, statusPage)
        logFile = '{}/{}'.format(logDir, statusPage)
        result = urllib.request.urlopen(url).read()
        if not os.path.exists(logDir):
            os.makedirs(logDir)
        with open(logFile, "w") as f:
            print(result, file=f)
        print("Wrote {} to {}".format(url, os.path.abspath(logFile)))

def main():
    config = configparser.ConfigParser()
    print("Read config from tattletale.conf")
    config.read('tattletale.conf')

    while True:
        checkConnection(config)
        # don't sleep -- that's done during LED display functions

def checkConnection(config: ConfigParser):
    routerUrl = config.get('urls', 'routerUrl')
    modemUrl = config.get('urls', 'modemUrl')
    externalUrl = config.get('urls', 'externalUrl')

    modemStatusPages = config.get('urls', 'modemStatusPages').split()
    logDir = config.get('logging', 'logDir')

    isRouterUp = isUp(routerUrl)
    isModemUp = isUp(modemUrl)
    isInternetUp = isUp(externalUrl)

    # We record these very raw observations here and more intelligent logic is done for each query
    writeDbEvent(config, isRouterUp, isModemUp, isInternetUp)

    # 4) grab modem status pages
    # TODO: Write to date stamped directory every so often OR every time the internet is down
    if not isInternetUp:
        grabStatus(modemUrl, modemStatusPages, logDir)

    # TODO: Send daily report email
    # TODO: Post to twitter
    # TODO: Create separate reporting program
    # TODO: Add speed test every N minutes

    # At the end, do some blocking LED operations for the on-board Raspberry Pi LED
    delaySec = 60
    if isInternetUp:
        show_led(sec=delaySec)
    elif not isRouterUp:
        blink_led_router_down(sec=delaySec)
    elif not isModemUp:
        blink_led_modem_down(sec=delaySec)
    elif not isInternetUp:
        blink_led_internet_down(sec=delaySec)
    else:
        print("ERROR: Unexpected state: Don't know how to blink the LED properly...")

if __name__ == "__main__":
    main()
