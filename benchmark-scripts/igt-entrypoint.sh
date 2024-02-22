#!/usr/bin/env bash
#
# Copyright (C) 2023 Intel Corporation.
#
# SPDX-License-Identifier: Apache-2.0
#

devices=$(/usr/local/bin/intel_gpu_top -L  | grep card | awk '{print $1,$5;}' | sed ":a;N;s/\n/@/g")
echo "devices found $devices"

IFS='@'
for device in $devices
do
    dev=$(echo $device | awk '{print $1}')
    echo "$dev"
    deviceId=$(echo $device | awk '{print $2}' | sed -E 's/.*?device=//' | cut -f1 -d",")
    echo "$deviceId"
    deviceNum=$(echo $dev | sed -E 's/.*?card//')
    echo "device number: $deviceNum"
    /usr/local/bin/intel_gpu_top -d pci:card=$deviceNum -J -s 1000 > /tmp/results/igt$deviceNum-$deviceId.json &
    echo "Starting igt capture for $device in igt$deviceNum-$deviceId.json"
done

while true
do
	echo "Capturing igt metrics"
	sleep 15
done