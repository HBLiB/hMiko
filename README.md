# hMiko
Ultimate Network Indexer (Junos &amp; Arista only for now)

1. Create a "devices.list" in the same directory with the devices in it, new line per device
2. Frist Run Scan.py, This this autodetect the OS's (It will only recognise Arista and Junos for now)
3. Run Update.py, there are some cases, like for the Juniper PTX, netmiko can't recognise the OS, and you would like to update the record manually.
4. Run ConfigGet.py, This will create a new json file with, OS type, running config, lldp (cli output and json format if available), interface description (cli output and json format if available) 
5. All the output will be saved as NetMikoOutput.json, all unreachable hosts are kept in (Config)Unreachable.lists
6. Run Analyse.py to lookup information, it will show it accordingly to the output. running config as you would see on the cli, and json format if availbale

This information then can be used further with pyvis to draw it.

