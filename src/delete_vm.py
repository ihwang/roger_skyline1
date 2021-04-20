from os         import system


def delete_vm(config):
    system("vboxmanage unregistervm " + config["VMNAME"] + " --delete")