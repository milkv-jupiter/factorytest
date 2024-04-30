#!/bin/bash -e

echo $1 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio$1/direction

while true
do
    echo 1 > /sys/class/gpio/gpio$1/value
    sleep 5
    echo 0 > /sys/class/gpio/gpio$1/value
    sleep 5
done