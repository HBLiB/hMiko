#!/usr/bin/env python3

import warnings
from cryptography.utils import CryptographyDeprecationWarning
with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=CryptographyDeprecationWarning)
    import paramiko
import getpass
import json
from netmiko import ConnectHandler
from jumpssh import SSHSession
import numpy as np
import threading
from netmiko.ssh_autodetect import SSHDetect
from netmiko.ssh_dispatcher import ConnectHandler
import threading
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
import time
from time import sleep

devicesRaw = []
devices = {}
finalDevices = {}
devList = []
notReachable = []
with open('devices.list') as f:
    devicesRaw = f.readlines()


for entry in devicesRaw:
    entry = entry.strip()
    devList.append(entry)

bastionServer = 'BASTION_IP'
user = input("Enter your username: ")
print("Enter your password")
passWord = getpass.getpass()


for entry in devicesRaw:
    entry = entry.strip()
    devices[entry] = {
    "device_type": "autodetect",
    "host": entry,
    "username": user,
    "password": passWord
    }

bastionConnect=paramiko.SSHClient()
bastionConnect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
bastionConnect.connect(bastionServer, username=user, password=passWord, port=22,timeout=10)
bastionTransport = bastionConnect.get_transport()
srcIP = (bastionServer, 22)

def sendCommand(dHost,dDict,dNotReachable):
    try:
        destIP = (dHost, 22)
        bastionChannel = bastionTransport.open_channel("direct-tcpip", destIP, srcIP,timeout=10)
        dDict[dHost]["sock"] = bastionChannel
        guess = SSHDetect(**dDict[dHost])
        best_match = guess.autodetect()
        #print (dHost)
        dDict[dHost]["device_type"] = best_match
        dDict[dHost].pop("sock", None)
        dDict[dHost].pop("username", None)
        dDict[dHost].pop("password", None)
    except Exception as err:
        paramiko.util.log_to_file('/dev/null')
        dNotReachable.append(dHost)
        dDict.pop(dHost, None)
    except OSError as error :
        #print(error)
        dNotReachable.append(dHost)
        dDict.pop(dHost, None)

threads = []
for host in devList:
    t= threading.Thread(target = sendCommand, args=(host,devices,notReachable,))
    t.start()
    threads.append(t)

while threading.active_count() > 2:
    print("still {} active threads ".format(threading.active_count()),end='\r')
    sleep(1)


print("",end='\r')
print("")
for t in threads:
    t.join()

print("Done",end='\r')

with open(r'unreachable.list', 'w') as fp:
    for item in notReachable:
        fp.write("%s\n" % item)
    print('Done')

with open("NetmikoDevices" +'.json', 'w') as fp:
    json.dump(devices, fp)
