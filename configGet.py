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


devices = {}
finalOutput = {}
devList = []
notReachable = []

with open("NetmikoDevices" +'.json', 'r') as jsonFile:
    devices = json.load(jsonFile)

for entry in devices.keys():
    entry = entry.strip()
    devList.append(entry)

bastionServer = 'BASTION_IP'
user = input("Enter your username: ")
print("Enter your password")
passWord = getpass.getpass()


bastionConnect=paramiko.SSHClient()
bastionConnect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
bastionConnect.connect(bastionServer, username=user, password=passWord, port=22,timeout=60)
bastionTransport = bastionConnect.get_transport()
srcIP = (bastionServer, 22)

def sendCommand(dHost,dDict,dNotReachable,dOutput):
    try:
        destIP = (dHost, 22)
        bastionChannel = bastionTransport.open_channel("direct-tcpip", destIP, srcIP,timeout=60)
        dDict[dHost]["username"] = user
        dDict[dHost]["password"] = passWord
        dDict[dHost]["sock"] = bastionChannel
        if dDict[dHost]['device_type'] == 'arista_eos':
            with ConnectHandler(**dDict[dHost]) as net_connect:
                dOutput[dHost]['device_type'] = dDict[dHost]['device_type']
                dOutput[dHost]['config'] = net_connect.send_command('show start')
                dOutput[dHost]['lldpRAW'] = net_connect.send_command('show lldp neighbors')
                dOutput[dHost]['descriptionRAW'] = net_connect.send_command('show interfaces description')
                dOutput[dHost]['lldp'] = json.loads(net_connect.send_command('show lldp neighbors | json'))
                dOutput[dHost]['description'] = json.loads(net_connect.send_command('show interfaces description | json'))
        elif dDict[dHost]['device_type'] == 'juniper_junos':
            with ConnectHandler(**dDict[dHost]) as net_connect:
                dOutput[dHost]['device_type'] = dDict[dHost]['device_type']
                dOutput[dHost]['config'] = net_connect.send_command('show configuration | display set')
                dOutput[dHost]['lldpRAW'] = net_connect.send_command('show lldp neighbors')
                dOutput[dHost]['descriptionRAW'] = net_connect.send_command('show interfaces descriptions')
                try:
                    dOutput[dHost]['lldp'] = json.loads(net_connect.send_command('show lldp neighbors | display json'))
                    dOutput[dHost]['description'] = json.loads(net_connect.send_command('show interfaces descriptions | display json'))
                except Exception as err:
                    pass
        dDict[dHost].pop("sock", None)
        dDict[dHost].pop("username", None)
        dDict[dHost].pop("password", None)
    except Exception as err:
        paramiko.util.log_to_file('/dev/null')
        dNotReachable.append(dHost)
    except OSError as error :
        dNotReachable.append(dHost)


threads = []

for host in devList:
    finalOutput[host] = {}
    t= threading.Thread(target = sendCommand, args=(host,devices,notReachable,finalOutput))
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

with open("NetMikoOutput" +'.json', 'w') as fp:
    json.dump(finalOutput, fp)

print (len(devices.keys()))
for item in notReachable:
    print(item)

with open(r'ConfigUnreachable.list', 'w') as fp:
    for item in notReachable:
        fp.write("%s\n" % item)
    print('Done')

bastionConnect.close()
