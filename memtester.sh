#!/bin/bash

test_size=100M
test_loop=1000

echo "Starting memtester..."
memtester $test_size $test_loop &

# Get the process ID of the memtester instance
memtester_pid=$!

# Wait for the process to finish
wait $memtester_pid

# Check the exit status of memtester process
if [ $? -eq 0 ]; then
    echo "memtester test completed successfully."
else
    echo "memtester test encountered an error or exited prematurely."
    echo none > /sys/class/leds/sys-led/trigger
fi
