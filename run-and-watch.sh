#!/bin/bash

run_prefix="$(echo -e "\e[34;1m  run.sh\e[0;1m: \e[0m")"
watch_prefix="$(echo -e "\e[35;1mwatch.sh\e[0;1m: \e[0m")"

./run.sh 2>&1 | sed "s/^/$run_prefix/g" &
sleep 2
./watch.sh 2>&1 | sed "s/^/$watch_prefix/g"
