#!/bin/bash

test_size=100M
test_loop=1

while true
do
    memtester $test_size $test_loop > /dev/null

    if [ $? -eq 0 ]; then
        echo "memtester test completed successfully."
    else
        echo "memtester test encountered an error or exited prematurely."
        echo none > /sys/class/leds/sys-led/trigger
        break
    fi
done
