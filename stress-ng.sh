#!/bin/bash

echo "Starting stress test..."
stress-ng --cpu 6 --cpu-method all --cpu-load 50 --metrics-brief &

# Get the process ID of the stress-ng instance
stress_ng_pid=$!

# Wait for the process to finish
wait $stress_ng_pid

# Check the exit status of stress-ng process
if [ $? -eq 0 ]; then
    echo "Stress test completed successfully."
else
    echo "Stress test encountered an error or exited prematurely."
    echo none > /sys/class/leds/sys-led/trigger
fi
