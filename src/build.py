from os import system

def build_image():
    system("cd ./iso && bash gen_preseed_iso.sh")