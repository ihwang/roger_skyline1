from os     import system


def start_vm(config):
    system("vboxmanage startvm " + config["VMNAME"])