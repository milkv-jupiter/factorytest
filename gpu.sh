#!/bin/bash

while true
do
    glmark2-es2-wayland --off-screen --run-forever > /tmp/glmark2.log
    if [ $? -eq 0 ]; then
        echo "gpu test completed successfully."
    else
        echo "gpu test encountered an error or exited prematurely."
        echo none > /sys/class/leds/sys-led/trigger
        break
    fi
done
