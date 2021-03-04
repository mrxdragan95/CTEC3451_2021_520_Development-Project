import subprocess 
import time
import os
import stat
import sys
import os.path
import shutil
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT

def clean_alert():
    print("Clean alert")
    os.system('cp /dev/null /var/log/snort/alert')
    os.system('rm -rf /var/log/snort/tcpdump.log*')

def new_folder_log(curr_time):
    func_name = "New folder to /tmp/snortlog"
    print(func_name)
    file_path = "/tmp/snortlog" + curr_time + "/"
    snortfile = os.path.dirname(file_path)

    try:
        os.stat(snortfile)
    except:
        os.mkdir(snortfile)

    print("New folder is done")


def run_tshark_on_local_machine(curr_time):
    func_name = "run_tshark_on_local_machine - "
    print(func_name + "start")
    interface_name = "eth0"
    capture_file_name = "/tmp/snortlog" + curr_time + "/" "Capture_" + interface_name + "_" + curr_time + ".pcap"
    num_sec_to_sleep = 115
    print(func_name + "about to create capture with name:" + capture_file_name)
    p = subprocess.Popen(["tshark",
                          "-i", interface_name,
                          "-w", capture_file_name, 
			  "host", "192.168.253.136"],
                           stdout=subprocess.PIPE)
    time.sleep(num_sec_to_sleep)
    p.terminate()
    print(func_name + "end")

def run_snort(curr_time):
    func_name = "run_snort - "
    print(func_name + "start")
    interface_name = "eth0"
    snortlog = "/var/log/snort"
    snortconf = "/etc/snort/snort.conf"
    capture_file_name = "/tmp/snortlog" + curr_time + "/" "Capture_" + interface_name + "_" + curr_time + ".pcap"
    num_sec_to_sleep = 15
    snort = subprocess.Popen(["snort", 
                          "-l", snortlog, "-c",
			  snortconf, "-r",
			  capture_file_name,
			  "-A", "fast"],
                          stdout=subprocess.PIPE)
    time.sleep(num_sec_to_sleep)
    snort.terminate()

def snortlog_to_txt(curr_time):
    file_line = "/tmp/snortlog" + curr_time + "/snortlog_line.txt"
    file = open(file_line, "w")
    num_sec_to_sleep = 3
    file.close()
    os.chmod(file_line, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)   
    shutil.copy('/var/log/snort/alert', file_line)
    time.sleep(num_sec_to_sleep)

def snortlog_to_pcap(curr_time):   
    reading_output = "/var/log/snort/tcpdump.log.*"
    capture_file_pcap = "/tmp/snortlog" + curr_time + "/" "snort_pcap_">
    num_sec_to_sleep = 3
    tcpdump = subprocess.Popen(["tshark", "-r", reading_output,
                                    "-w", capture_file_pcap],
                                    stdout=subprocess.PIPE)
    time.sleep(num_sec_to_sleep)
    tcpdump.terminate()

                        

clean_alert()
curr_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
os.system('systemctl stop snort')
new_folder_log(curr_time)
run_tshark_on_local_machine(curr_time)
run_snort(curr_time)
snortlog_to_txt(curr_time)
snortlog_to_pcap(curr_time)
print("Done")
