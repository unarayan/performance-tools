#!/bin/bash

# Get all lines containing pci: and both device= and card=
mapfile -t pci_devices < <(intel_gpu_top -L | grep -E 'pci:.*device=.*card=')

if [ ${#pci_devices[@]} -eq 0 ]; then
    echo "No valid PCI GPU devices with both device ID and card number found."
    exit 1
fi

for device_line in "${pci_devices[@]}"; do
    # Extract the card name (e.g., card1)
    card=$(echo "$device_line" | awk '{print $1}')

    # Extract the full pci string (starting from "pci:")
    pci_info=$(echo "$device_line" | grep -o 'pci:[^ ]*')

    # Extract device ID and card number
    device_id=$(echo "$pci_info" | sed -n 's/.*device=\([0-9A-Fa-f]*\).*/\1/p')
    card_num=$(echo "$pci_info" | sed -n 's/.*card=\([0-9]*\).*/\1/p')

    if [[ -n "$device_id" && -n "$card_num" ]]; then
        echo "Valid device found: $card | Device ID: $device_id | Card Number: $card_num"

        output_file="/tmp/results/igt${card_num}-${device_id}.csv"
        touch "$output_file"
        chown 1000:1000 "$output_file"

        echo "Starting igt capture to $output_file"
        intel_gpu_top -d pci:card=$card_num -c -o "$output_file" &
    else
        echo "Skipping $card: Incomplete pci info"
    fi
done

# Continuous logging
while true; do
    echo "Capturing igt metrics..."
    sleep 15
done