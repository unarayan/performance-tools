.PHONY: build-all build-platform build-igt build-xpum run-platform run-igt run-xpum

build-all: build-platform build-igt build-xpum

build-platform:
	echo "Building benchmark container HTTPS_PROXY=${HTTPS_PROXY} HTTP_PROXY=${HTTP_PROXY}"
	cd platform && docker build --build-arg HTTPS_PROXY=${HTTPS_PROXY} --build-arg HTTP_PROXY=${HTTP_PROXY} -t benchmark:platform -f Dockerfile .

build-igt:
	echo "Building igt HTTPS_PROXY=${HTTPS_PROXY} HTTP_PROXY=${HTTP_PROXY}"
	cd intel-top && docker build --build-arg HTTPS_PROXY=${HTTPS_PROXY} --build-arg HTTP_PROXY=${HTTP_PROXY} -t benchmark:igt -f Dockerfile .

build-xpum:
	echo "Building xpu HTTPS_PROXY=${HTTPS_PROXY} HTTP_PROXY=${HTTP_PROXY}"
	cd xpum && docker build --build-arg HTTPS_PROXY=${HTTPS_PROXY} --build-arg HTTP_PROXY=${HTTP_PROXY} -t benchmark:xpu -f Dockerfile .

run-platform:
	docker run -d --rm --name=platform -v `pwd`/results:/tmp/results --privileged benchmark:platform

run-igt:
	docker run -d --rm --name=igt -v `pwd`/results:/tmp/results --privileged benchmark:igt

run-xpum:
	docker run -itd -v /sys/firmware/acpi/tables/MCFG:/pcm/sys/firmware/acpi/tables/MCFG:ro -v /proc/bus/pci/:/pcm/proc/bus/pci/ -v /proc/sys/kernel/nmi_watchdog:/pcm/proc/sys/kernel/nmi_watchdog -v `pwd`/results:/tmp/xpumdump/  --cap-drop ALL --cap-add CAP_SYS_ADMIN --user root -e XPUM_REST_NO_TLS=1 --device /dev/dri:/dev/dri --device /dev/cpu:/dev/cpu --name=xpum benchmark:xpu
