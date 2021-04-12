#!/bin/bash

#sudo apt-get update; sudo apt-get install bsdtar gunzip gzip md5sum cpio genisoimage curl -y

#curl -o mini.iso http://ftp.debian.org/debian/dists/sid/main/installer-amd64/current/images/netboot/mini.iso


PRESEED_DIR=mini_preseed


mkdir ./${PRESEED_DIR}
bsdtar -C ./${PRESEED_DIR} -xf mini.iso
chmod +w ./${PRESEED_DIR}/initrd.gz
gunzip ./${PRESEED_DIR}/initrd.gz
echo preseed.cfg | cpio -H newc -o -A -F ./${PRESEED_DIR}/initrd
gzip ./${PRESEED_DIR}/initrd
chmod -w ./${PRESEED_DIR}/initrd.gz

cd ./${PRESEED_DIR}
find -follow -type f ! -name md5sum.txt -print0 | xargs -0 md5sum > md5sum.txt
chmod -w md5sum.txt
cd ..

sudo genisoimage    -r -J -b isolinux.bin -c boot.cat \
                    -no-emul-boot -boot-load-size 4 -boot-info-table \
                    -o mini_preseed.iso ./${PRESEED_DIR}
#sudo rm -rf ./${PRESEED_DIR}