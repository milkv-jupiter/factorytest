#!/bin/bash

test_size=100M
test_loop=1

while true
do
    memtester $test_size $test_loop
    [ $? -eq 0 ] || exit -1
done