from os     import system, popen
from time   import sleep

import sys


DISK_INTERFACES = ("IDE", "SATA")


def create_vm(config):
    system("vboxmanage createvm --name " + config["VMNAME"] \
    + " --ostype " + config["OSTYPE"] + " --register")
    system("vboxmanage modifyvm " + config["VMNAME"] \
    + " --memory " + config["RAM"] + " --cpus " + config["CPU_CORE"])


def set_preseed(config):
    pass


def set_storage(config):
    for interface in DISK_INTERFACES:
        system("vboxmanage storagectl " + config["VMNAME"] \
            + " --name " + interface + " --add " + interface)
    system("vboxmanage createmedium disk" \
        + " --filename /tmp/" + config["VMNAME"] \
        + " --format " + config["DISK_FORMAT"] \
        + " --size " + config["DISK_SIZE"])
    system("vboxmanage storageattach " + config["VMNAME"] \
        + " --storagectl " + DISK_INTERFACES[0] \
        + " --port 0 --device 0 --type dvddrive" \
        + " --medium " + config["ISO_PATHNAME"])
        # ISO should be generated
    system("vboxmanage storageattach " + config["VMNAME"] \
        + " --storagectl " + DISK_INTERFACES[1] + " --port 0 --device 0" \
        + " --type " + config["DISK_TYPE"] \
        + " --medium /tmp/" + config["VMNAME"] + ".vdi")


def set_bootorder(vmname):
    system("vboxmanage modifyvm " + vmname \
        + " --boot1 dvd --boot2 disk")


def set_network(config):
    system("vboxmanage modifyvm " + config["VMNAME"] + " --nic1 bridged")
    # promiscuous mode setting
    # system("vboxmanage modifyvm " + config["VMNAME"] + " --nicpromisc1 allow-all")
    # cable-like mode
    # system("vboxmanage modifyvm " + config["VMNAME"] + " --cableconnected1 on")
    system("vboxmanage modifyvm " +config["VMNAME"] + " --bridgeadapter1 enp0s25")


def install_os(config):
    system("vboxmanage startvm " + config["VMNAME"])
    # system("vboxmanage startvm " + config["VMNAME"] + " --type headless")
    sleep(1)
    status = popen("vboxmanage showvminfo " + config["VMNAME"] \
        + " | grep -c 'running'").read()
    if '0' in status:
        print("roger_skyline_1: Can't run VM " + config["VMNAME"], file=sys.stderr)
        exit()
    else:
        print("Installing Operating System to VM " + config["VMNAME"])
        while True:
            is_running = popen("vboxmanage showvminfo " + config["VMNAME"] \
                + " | grep -c 'running'").read()
            if '1' in status:
                sleep(5)
            else:
                print("Operating System Installed")
                break
        detach_device("IDE", config["VMNAME"])


def detach_device(device, vmname):
    system("vboxmanage storageattach " + vmname \
        + " --storagectl " + device + " --port 0 --device 0 -- medium none")


def share_key(config):
    system("cp ~/.ssh/id_rsa.pub ./mykey")
    system("git add mykey; git commit -m 'update key'; git push")


def stop_share_key(config):
    system("rm ./mykey")
    system("git add .; git commit -m 'stop sharing key' ; git push")


def setup_vm(config):
    create_vm(config)
    set_preseed(config)
    set_storage(config)
    set_bootorder(config["VMNAME"])
    set_network(config)
    share_key(config)
    install_os(config)
    stop_share_key(config)
