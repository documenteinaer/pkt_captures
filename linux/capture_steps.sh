#!/bin/sh 

step=1

while true; do
    sjson=$(printf "%03d.json" $step)
    ./capture.py 2> /dev/null  > $sjson

    echo "captured step $step
press ENTER to start"
    read fakevar 
    step=$(($step + 1))
    
done 
