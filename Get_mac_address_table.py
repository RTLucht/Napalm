import json
from getpass import getpass
from napalm import get_network_driver


IP = input("Enter IP adress seperated by a space: ")
username = input('Enter your username: ')
password = getpass()

devices = IP.split()



for ip_address in devices:
    print ("Connecting to " + str(ip_address))
    driver = get_network_driver('ios')
    iosv = driver(ip_address, username, password)


    iosv.open()
    ios_output = iosv.get_mac_address_table()
    print (json.dumps(ios_output, sort_keys=True, indent=4))


    iosv.close()
