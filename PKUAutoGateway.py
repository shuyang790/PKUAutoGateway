#!/usr/bin/env python3

# PKUAutoGateway
#   Should work on Linux/Unix
#   Tested only on macOS for now
# Contact: Shuyang S. shuyang790@gmail.com

import requests
import json
import subprocess
import getpass
import time
import datetime

url = "https://its.pku.edu.cn/cas/ITSClient"

proxies = {
    'http': '',
    'https': '',
}

username = input('username (student ID): ')
password = getpass.getpass()

lastIP = ''

headersTemplate = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "app": "IPGWiOS1.2",
        "cmd": "open",
        "username": username,
        "password": password,
}


def checkNetwork(url='http://www.baidu.com/', timeout=1):
    try:
        req = requests.head(url, timeout=timeout, proxies=proxies)
        # HTTP errors are not raised by default, this statement does that
        req.raise_for_status()
        return True
    except requests.HTTPError as e:
        print ("Checking internet connection failed, status code {0}.".format(
            e.response.status_code
        ))
    except requests.ConnectionError:
        print ("No internet connection available.")
    return False


def getCurrentIP(type=4):
    if type == 4:
        res = subprocess.check_output(
            'ifconfig en0 | grep "inet " | awk \'{print($2)}\'',
            shell=True,
        ).decode('utf-8').replace('\n', '')
    else:
        res = subprocess.check_output(
            'ifconfig en0 | grep "inet6 " | grep "autoconf secured" '
            '| awk \'{print($2)}\'',
            shell=True,
        ).decode('utf-8').replace('\n', '')
    return res


def printJSON(obj):
    print (datetime.datetime.now())
    print (json.dumps(
        obj,
        indent=4,
        separators=(',', ': '),
        ensure_ascii=False,
    ))


def disconnectAll():
    headers = headersTemplate
    headers["cmd"] = "close"
    res = json.loads(
        requests.post(url, headers, proxies=proxies, timeout=1).text
    )
    printJSON(res)


def disconnectOne(ip=lastIP):
    if ip == '':
        return
    headers = headersTemplate
    headers["ip"] = ip
    headers["cmd"] = "disconnect"
    res = json.loads(
        requests.post(url, headers, proxies=proxies, timeout=1).text
    )
    printJSON(res)


def getConnections():
    headers = headersTemplate
    headers["cmd"] = "getconnections"
    res = json.loads(
        requests.post(url, headers, proxies=proxies, timeout=1).text
    )
    printJSON(res)


def connect(range="free"):
    if range != "free":
        range = "fee"
    headers = headersTemplate
    headers["iprange"] = range
    headers["cmd"] = "open"
    while True:
        res = json.loads(
            requests.post(url, headers, proxies=proxies, timeout=1).text
        )
        printJSON(res)
        if res["SCOPE"] in ["domestic", "international"]:
            global lastIP
            lastIP = res["IP"]
            break
        disconnectOne()


def main():
    printNow = True
    while True:
        if getCurrentIP().startswith('10.') and not checkNetwork():
            try:
                connect()
            except:
                pass
        elif printNow:
            printNow = False
            print ("Already connected to network with IP address {}".format(
                getCurrentIP()
            ))
        time.sleep(20)

if __name__ == "__main__":
    main()
