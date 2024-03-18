#!/usr/bin/env bash
#
# Copyright (C) 2024 Intel Corporation.
#
# SPDX-License-Identifier: Apache-2.0
#

# shellcheck disable=SC2086 # Intended work splitting
devices=$(/usr/local/bin/intel_gpu_top -L  | grep card | awk '{print $1,$5;}' | sed ":a;N;s/\n/@/g")
echo "devices found $devices"

if [ -z "$devices" ]
then
    echo "No valid GPU devices found"
	exit 1
fi

IFS='@'
for device in $devices
do
    # shellcheck disable=SC2086 # Intended work splitting
    dev=$(echo $device | awk '{print $1}')
    echo "$dev"
    # shellcheck disable=SC2086 # Intended work splitting
    deviceId=$(echo $device | awk '{print $2}' | sed -E 's/.*?device=//' | cut -f1 -d",")
    echo "$deviceId"
    # shellcheck disable=SC2086 # Intended work splitting
    deviceNum=$(echo $dev | sed -E 's/.*?card//')
    echo "device number: $deviceNum"
    touch /tmp/results/igt$deviceNum-$deviceId.json
    chown 1000:1000 /tmp/results/igt$deviceNum-$deviceId.json
    # shellcheck disable=SC2086 # Intended work splitting
    echo "Starting igt capture for $device in igt$deviceNum-$deviceId.json"
    /usr/local/bin/intel_gpu_top -d pci:card=$deviceNum -J -s 1000 > /tmp/results/igt$deviceNum-$deviceId.json
done
