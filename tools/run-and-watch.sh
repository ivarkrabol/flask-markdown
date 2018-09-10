#!/usr/bin/env bash
set -e

function run-and-watch {
  (make run 2>&1 \
    | while read line; \
        do echo -e "  run: $line"; \
        done ) &
  RUN_JOB=$!
  trap "kill $RUN_JOB" SIGINT SIGTERM EXIT
  (make watch 2>&1 \
    | while read line; \
        do echo -e "watch: $line"; \
        done ) &
  WATCH_JOB=$!
  trap "kill $RUN_JOB $WATCH_JOB 2> /dev/null" SIGINT SIGTERM EXIT
  wait $RUN_JOB $WATCH_JOB
}

make prepare
real_run_label="$(printf "\e[34m  run\e[0m:")"
real_wtc_label="$(printf "\e[35mwatch\e[0m:")"
run-and-watch | sed -e "s/^  run:/${real_run_label}/" -e "s/^watch:/${real_wtc_label}/"
