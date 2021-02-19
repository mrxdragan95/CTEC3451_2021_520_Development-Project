import subprocess
import time
import os
import stat
import sys
import os.path
import shutil
from datetime import datetime

def run_tshark_on_local_machine(curr_time):
    func_name = "run_tshark_on_local_machine - "
    print(func_name + "start")
    interface_name = "eth0"
    capture_file_name = "/tmp/Capture_interface_" + interface_name + "_" + curr_time + ".pcap"
    num_sec_to_sleep = 290
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
    capture_file_name = "/tmp/Capture_interface_" + interface_name+ "_" + curr_time + ".pcap"
    num_sec_to_sleep = 20
    s = subprocess.Popen(["snort", 
                          "-l", snortlog, "-c",
			  snortconf, "-r",
			  capture_file_name, 
			  "-A", "full"],
                          stdout=subprocess.PIPE)
    time.sleep(num_sec_to_sleep)
    s.terminate()

def snortlog_to_txt(curr_time):
    func_name = "Move to /tmp/snortlog"
    print(func_name)
    file_path = "/tmp/snortlog" + curr_time + "/"
    snortfile = os.path.dirname(file_path)

    try:
        os.stat(snortfile)
    except:
        os.mkdir(snortfile)

    file_line = "/tmp/snortlog" + curr_time + "/snortlog_line.txt"
    file = open(file_line, "w")
    file.close()
    os.chmod(file_line, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)   
    shutil.copy('/var/log/snort/alert', file_line)

    #file_cat = "/tmp/snortlog" + curr_time + "/snortlog_cat.txt"
    #file = open(file_cat, "w")
    #file.close()
    #os.chmod(file_cat, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
    #shutil.copy('/var/log/snort/alert', cat_line)

    print("Done!")


curr_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
os.system('systemctl stop snort')
run_tshark_on_local_machine(curr_time)
run_snort(curr_time)
snortlog_to_txt(curr_time)
print("Done")
