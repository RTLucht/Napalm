import json
import sys
from napalm import get_network_driver
from netmiko import ConnectHandler
from getpass import getpass


#This will ask you to input IP address of switch your username and password to access the 
#devices 
IP = input("Enter IP adress seperated by a space: ")
username = input('Enter your username: ')
password = getpass()

devices = IP.split()

#List of network switches to send the command to


Confirm = input("Would you like to actually do this? (y/N) ").lower()

# Check if our answer is y or n, really anything other than y will kick you out
if Confirm != ('y'):
    # call method
    exit()



for ip_address in devices:
    print ('Enabling IP SCP on" ' + ip_address)

    ios_device = {
        'device_type': 'cisco_ios',
        'ip': ip_address, 
        'username': username,
        'password': password
    }

    net_connect = ConnectHandler(**ios_device)
    output = net_connect.send_config_set('ip scp server enable')


for ip_address in devices:
    print ("Connecting to " + str(ip_address))
    driver = get_network_driver('ios')
    iosv = driver(ip_address, username, password)
    iosv.open()
    #this is a text document and location of commands to send to the 
    #devices in the devicelist
    iosv.load_merge_candidate(filename='LAB.txt')
    diffs = iosv.compare_config()
    #will compare the commands to the current config and apply only 
    #what will change, if the current config already has the new commands
    #the changes will be ignored
    if len(diffs) > 0:
        print(diffs)
        iosv.commit_config()
    else:
        #If nothing needs to be added then no changes are made
        print('No config changes required.')
        iosv.discard_config()



    iosv.close()




