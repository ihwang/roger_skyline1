#!/bin/bash

PRESEED_DIR="temp_isofiles"
ORIGINAL_ISO="mini.iso"
PRESEEDED_ISO="preseed-mini.iso"


function do_prepare() {
	sudo apt-get update
	sudo apt-get install bsdtar -y
	sudo apt-get install gunzip -y
	sudo apt-get install gzip -y
	sudo apt-get install md5sum -y
	sudo apt-get install cpio -y
	sudo apt-get install genisoimage -y
	sudo apt-get install curl -y
	curl -O http://ftp.debian.org/debian/dists/buster/main/installer-amd64/current/images/netboot/mini.iso
}

function do_unzip() {
	mkdir ./${PRESEED_DIR}
	bsdtar -C ./${PRESEED_DIR} -xf ${ORIGINAL_ISO}
	chmod +w ./${PRESEED_DIR}/initrd.gz
	sudo gunzip ./${PRESEED_DIR}/initrd.gz
}

function do_preseed() {
	cp -f isolinux.cfg ./${PRESEED_DIR}
}

function do_rezip() {
	sudo gzip ./${PRESEED_DIR}/initrd
	chmod -w ./${PRESEED_DIR}/initrd.gz
	cd ./${PRESEED_DIR}
	find -follow -type f ! -name md5sum.txt -print0 | xargs -0 md5sum > md5sum.txt
	chmod -w md5sum.txt
	cd ..
	sudo genisoimage    -r -J -b isolinux.bin -c boot.cat \
						-no-emul-boot -boot-load-size 4 -boot-info-table \
	                    -o ${PRESEEDED_ISO} ./${PRESEED_DIR}
	sudo rm -rf ./${PRESEED_DIR}
}

#do_prepare
do_unzip
do_preseed
do_rezip
