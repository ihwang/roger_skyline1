from os     import system


def install_pkgs(config):
    system("ssh -i ~/.ssh/id_rsa debian@" + config["IP"] + " 'sh -s' < ./scripts/install_pkgs.sh root debian")


def config_os(config):
    # install_pkgs(config)
    pass