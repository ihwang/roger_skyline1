import sys
from os     import system, popen
from time   import sleep


DISK_INTERFACES = ("IDE", "SATA")


def create_vm(config):
    system("vboxmanage createvm --name " + config["VMNAME"] \
    + " --ostype " + config["OSTYPE"] + " --register")
    system("vboxmanage modifyvm " + config["VMNAME"] \
    + " --memory " + config["RAM"] + " --cpus " + config["CPU_CORE"])


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
    system("vboxmanage storageattach " + config["VMNAME"] \
        + " --storagectl " + DISK_INTERFACES[1] + " --port 0 --device 0" \
        + " --type " + config["DISK_TYPE"] \
        + " --medium /tmp/" + config["VMNAME"] + ".vdi")


def set_bootorder(vmname):
    system("vboxmanage modifyvm " + vmname \
        + " --boot1 dvd --boot2 disk")


def set_network(config):
    system("vboxmanage modifyvm " + config["VMNAME"] + " --nic1 bridged")
#    system("vboxmanage modifyvm " + config["VMNAME"] + " --cableconnected1 on")
    system("vboxmanage modifyvm " +config["VMNAME"] + " --bridgeadapter1 enp0s25")


def setup_vm(config):
    status = system("vboxmanage showvminfo " + config["VMNAME"] + " >/dev/null 2>&1")
    if status == 0:
        print("roger_skyline_1: the virtual machine " + config["VMNAME"] + " has already been set up", file=sys.stderr)
        exit(1)
    create_vm(config)
    set_storage(config)
    set_bootorder(config["VMNAME"])
    set_network(config)
