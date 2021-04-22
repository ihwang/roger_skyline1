from os         import system, popen
from time       import sleep
import sys


def connect_ssh(config, boot):
    if boot == 1:
        print("roger_skyline_1: Booting " + config["VMNAME"] + "..")
        system("vboxmanage controlvm " + config["VMNAME"] + " acpipowerbutton >/dev/null 2>&1")
        sleep(3)
        system("vboxmanage startvm " + config["VMNAME"] + " --type headless >/dev/null 2>&1")
        sleep(3)
    is_running = popen("vboxmanage showvminfo " + config["VMNAME"] \
        + " | grep -c 'running'").read()
    if is_running[0] == '0':
        print("roger_skyline_1: The VM " + config["VMNAME"] + "is not running. Use '--boot' option or boot " + config["VMNAME"] + " manually.", file=sys.stderr)
        exit()
    else:
        while system("ping -c 1 -t 2 " + config["IP"] + " >/dev/null 2>&1"):
            sleep(1)
        sleep(1)
        print("roger_skyline_1: Connecting to ssh..")
        system("ssh -p " + config["SSH_PORT"] + " debian@" + config["IP"])
