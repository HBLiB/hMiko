#!/usr/bin/env python3

import json

with open("NetmikoDevices" +'.json', 'r') as jsonFile:
    devices = json.load(jsonFile)


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


print (color.RED +  "Unknown Device Type Nodes:"+ color.END)
for x in devices.keys():
    if not devices[x]['device_type']:
        print(x)


print(color.RED +  'Would you like to Update the device type manually?'+ color.END)
while True:
    dupdate = input(color.RED +  "yes/no:\n"+ color.END)
    if dupdate == "yes":
        host = input(color.RED +  "Which Device?\n"+ color.END)
        os = input(color.RED +  "Which OS? ( juniper_junos / arista_eos)\n"+ color.END)
        devices[host]['device_type'] = os
        print(color.RED +  'Would you like to Update another node?'+ color.END)
        for x in devices.keys():
            if not devices[x]['device_type']:
                print(x)
    if dupdate == "no":
        break


print (color.RED +  "Unknown Device Type Nodes:"+ color.END)
for x in devices.keys():
    if not devices[x]['device_type']:
        print(x)

with open("NetmikoDevices" +'.json', 'w') as fp:
    json.dump(devices, fp)
