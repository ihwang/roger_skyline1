import sys
sys.dont_write_bytecode = True

import os

from src.parser         import parser
from src.build          import build_image
from src.setup_vm       import setup_vm
# from src.stop_vm        import stop_vm
# from src.delete_vm      import delete_vm
# from src.connect_ssh    import connect_ssh


CONFIG_FILE = "./config/roger_skyline_1.cfg"


def main():
    if len(sys.argv) != 2:
        print("roger_skyline_1: usage: roser_skyline_1 <command> ", file=sys.stderr)
        # introducing command
        exit(1)
    if os.access(CONFIG_FILE, os.R_OK) == False:
        print("roger_skyline: can't read configuration file", file=sys.stderr)
        exit(1)
    config = parser(CONFIG_FILE)
    if sys.argv[1] == 'build':
        build_image(config)
    elif sys.argv[1] == 'setup':
        setup_vm(config)
    elif sys.argv[1] == 'start':
        start_vm(config)
    elif sys.argv[1] == 'stop':
        stop_vm(config)
    elif sys.argv[1] == 'delete':
        delete_vm(config)
    elif sys.argv[1] == 'connect':
        connect_ssh(config)


if __name__ == '__main__':
    main()
