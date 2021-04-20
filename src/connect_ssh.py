from os         import system


def connect_ssh(config):
    system("ssh debian@" + config["IP"])
