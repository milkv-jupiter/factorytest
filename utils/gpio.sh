#!/bin/bash -e

for gpio in "$@"
do
    echo $gpio > /sys/class/gpio/export
    echo out > /sys/class/gpio/gpio$gpio/direction
    echo 1 > /sys/class/gpio/gpio$gpio/value
done
