import os
import sys

def build_image(config):
    # iso_pathname = config["ISO_PATHNAME"].replace("\"", "")
    iso_pathname = config["ISO_PATHNAME"].strip()
    if os.access(iso_pathname, os.F_OK):
        print("roger_skyline1: \"" + iso_pathname + "\" file has already been created", file=sys.stderr)
        exit(1)
    os.system("cd ./iso && bash gen_preseed_iso.sh")
