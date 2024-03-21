# Copyright © 2024 Intel Corporation. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

.PHONY: build-all build-platform build-igt build-xpum run-platform run-igt run-xpum start-performance-tools stop-performance-tools

build-all: build-platform build-igt build-xpum

build-platform:
	echo "Building benchmark container HTTPS_PROXY=${HTTPS_PROXY} HTTP_PROXY=${HTTP_PROXY}"
	cd platform && docker build --build-arg HTTPS_PROXY=${HTTPS_PROXY} --build-arg HTTP_PROXY=${HTTP_PROXY} -t benchmark:platform -f Dockerfile .

build-igt:
	echo "Building igt HTTPS_PROXY=${HTTPS_PROXY} HTTP_PROXY=${HTTP_PROXY}"
	cd intel-top && docker build --build-arg HTTPS_PROXY=${HTTPS_PROXY} --build-arg HTTP_PROXY=${HTTP_PROXY} -t benchmark:igt -f Dockerfile .

build-xpum:
	echo "Building xpu HTTPS_PROXY=${HTTPS_PROXY} HTTP_PROXY=${HTTP_PROXY}"
	cd xpum && docker build --build-arg HTTPS_PROXY=${HTTPS_PROXY} --build-arg HTTP_PROXY=${HTTP_PROXY} -t benchmark:xpum -f Dockerfile .

run-platform:
	docker run -d --rm --name=platform -v `pwd`/results:/tmp/results --privileged benchmark:platform

run-igt:
	docker run -d --rm --name=igt -v `pwd`/results:/tmp/results --privileged benchmark:igt
 
run-xpum:
	docker run -d --rm -v /sys/firmware/acpi/tables/MCFG:/pcm/sys/firmware/acpi/tables/MCFG:ro -v /proc/bus/pci/:/pcm/proc/bus/pci/ -v /proc/sys/kernel/nmi_watchdog:/pcm/proc/sys/kernel/nmi_watchdog -v `pwd`/results:/tmp/xpumdump/ --privileged --user=root -e XPUM_REST_NO_TLS=1 --device /dev/dri:/dev/dri --device /dev/cpu:/dev/cpu --name=xpum benchmark:xpum

start-performance-tools:
	log_dir=./results docker compose up

stop-performance-tools:
	log_dir=./results docker compose down