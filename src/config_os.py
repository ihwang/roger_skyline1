from os     import system
from time   import sleep


def config_os(config):
    print("roger_skyline_1: Configuring OS..")
    system("vboxmanage startvm " + config["VMNAME"] \
        + " --type headless >/dev/null 2>&1")
    while system("ping -c 1 -t 2 " + config["IP"] + " >/dev/null 2>&1"):
        sleep(1)
    system("ssh -i ~/.ssh/id_rsa debian@" + config["IP"] \
        + " 'sh -s' < ./config/config_os.sh root debian " + config["SSH_PORT"])
    system("vboxmanage controlvm " + config["VMNAME"] + " acpipowerbutton")
