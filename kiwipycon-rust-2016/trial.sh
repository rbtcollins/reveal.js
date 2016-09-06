#!/bin/bash
# Run two programs a few times and compare the durations.
# Depends on ministat.

numargs=$#
cmd="ministat -s -w 50"
for ((i=1 ; i <= numargs ; i++))
do
  truncate --size=0 trial.$i
  # 10 iterations.
  for ignored in $(seq 10); do
    /usr/bin/time --quiet -f "%e" $1 2>> trial.$i
  done
  cmd="$cmd trial.$i"
  shift
done

$cmd
