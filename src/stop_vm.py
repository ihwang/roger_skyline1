from os         import system


def stop_vm(config):
    system("vboxmanage controlvm " + config["VMNAME"] + " acpipowerbutton")