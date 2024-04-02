# Copyright © 2024 Intel Corporation. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

ROOT_DIRECTORY ?= results

consolidate:
	python3 consolidate_multiple_run_of_metrics.py --root_directory $(ROOT_DIRECTORY)/ --output $(ROOT_DIRECTORY)/summary.csv

python-test:
	python -m coverage run -m unittest benchmark_test.py

python-integration:
	python -m coverage run -m unittest benchmark_integration.py

python-coverage:
	coverage report -m