from os     import system
from time   import sleep

def load_script(config):
    sleep(1)
    system("ssh-copy-id -i ~/.ssh/id_rsa.pub debian@" + config["IP"])
    sleep(1)
    system("ssh -i ~/.ssh/id_rsa debian@" + config["IP"] \
        + " 'sh -s' < ./config/config_os.sh root debian " + config["SSH_PORT"])
 

def config_os(config):
    print("roger_skyline_1: Configuring OS..")
    system("vboxmanage startvm " + config["VMNAME"] \
        + " --type headless >/dev/null 2>&1")
    while system("ping -c 1 -t 2 " + config["IP"] + " >/dev/null 2>&1"):
        sleep(1)
    load_script(config)
    system("vboxmanage controlvm " + config["VMNAME"] + " acpipowerbutton")
