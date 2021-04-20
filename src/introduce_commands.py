def introduce_commands():
    print("-----------------------Available commands--------------------------")
    print("build: Download 'mini.iso' file and preseed 'preseed.cfg' file.")
    print("setup: Create VM, Install os based on '.iso' file has been generated" \
        + " from 'build' command and configure VM.")
    print("start: Run VM in Virtualbox emulator.")
    print("stop: Stop the running VM.")
    print("delete: Delete VM.")
    print("connect: Connect to VM via SSH.")
    print("help or ?: Repeat this introduction.")
