import os
import sys

def build_image():
    os.system("cd ./iso && bash gen_preseed_iso.sh")
