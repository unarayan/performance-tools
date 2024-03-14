#!/usr/bin/env bash
#
# Copyright (C) 2023 Intel Corporation.
#
# SPDX-License-Identifier: Apache-2.0
#

echo "Starting platform data collection"

echo "Starting sar collection"
sar 1 >& /tmp/results/cpu_usage.log &

echo "Starting free collection"
free -s 1 >& /tmp/results/memory_usage.log &

echo "Starting iotop collection"
iotop -o -P -b >& /tmp/results/disk_bandwidth.log &

echo "Starting xeon pcm-power collection"
/opt/intel/pcm-bin/bin/pcm 1 -silent -nc -nsys -csv=/tmp/results/pcm.csv &

while true
do
	echo "Capturing system metrics"
	sleep 15
done