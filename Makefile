# Copyright © 2023 Intel Corporation. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

.PHONY: build-all build-benchmark build-xpu build-igt run consolidate

MKDOCS_IMAGE ?= asc-mkdocs

build-all: build-benchmark build-xpu build-igt

build-benchmark:
	echo "Building benchmark container HTTPS_PROXY=${HTTPS_PROXY} HTTP_PROXY=${HTTP_PROXY}"
	cd benchmark-scripts && docker build --build-arg HTTPS_PROXY=${HTTPS_PROXY} --build-arg HTTP_PROXY=${HTTP_PROXY} -t benchmark:dev -f Dockerfile.benchmark .

build-xpu:
	echo "Building xpu HTTPS_PROXY=${HTTPS_PROXY} HTTP_PROXY=${HTTP_PROXY}"
	cd benchmark-scripts && docker build --build-arg HTTPS_PROXY=${HTTPS_PROXY} --build-arg HTTP_PROXY=${HTTP_PROXY} -t benchmark:xpu -f Dockerfile.xpu .

build-igt:
	echo "Building igt HTTPS_PROXY=${HTTPS_PROXY} HTTP_PROXY=${HTTP_PROXY}"
	cd benchmark-scripts && docker build --build-arg HTTPS_PROXY=${HTTPS_PROXY} --build-arg HTTP_PROXY=${HTTP_PROXY} -t benchmark:igt -f Dockerfile.igt .

run:
	cd benchmark-scripts && docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock -v `pwd`/results:/tmp/results --net=host --privileged benchmark:dev /bin/bash

consolidate:
	cd benchmark-scripts && docker run -itd -v `pwd`/$(ROOT_DIRECTORY):/$(ROOT_DIRECTORY) -e ROOT_DIRECTORY=$(ROOT_DIRECTORY)--net=host --privileged benchmark:dev /bin/bash -c "python3 consolidate_multiple_run_of_metrics.py --root_directory $(ROOT_DIRECTORY)/ --output $(ROOT_DIRECTORY)/summary.csv"


docs: clean-docs
	mkdocs build
	mkdocs serve -a localhost:8008

docs-builder-image:
	docker build \
		-f Dockerfile.docs \
		-t $(MKDOCS_IMAGE) \
		.

build-docs: docs-builder-image
	docker run --rm \
		-v $(PWD):/docs \
		-w /docs \
		$(MKDOCS_IMAGE) \
		build

serve-docs: docs-builder-image
	docker run --rm \
		-it \
		-p 8008:8000 \
		-v $(PWD):/docs \
		-w /docs \
		$(MKDOCS_IMAGE)