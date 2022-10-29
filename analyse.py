#!/usr/bin/env python3

import json

with open("NetMikoOutput" +'.json', 'r') as jsonFile:
    devices = json.load(jsonFile)

devicesList = list(devices.keys())

columns = 3

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



for first, second, third in zip(devicesList[::columns], devicesList[1::columns], devicesList[2::columns]):
    print(f'{first: <60}{second: <60}{third}')


user = input(color.BOLD +  "Which Device do you want to see?\n" + color.END)
for x in devices[user].keys():
    print ("----",x)
info = input(color.RED + "What info do you want to see?\n"+ color.END)

print (devices[user][info])
