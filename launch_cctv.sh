#!/bin/bash

# launch_cctv.sh
# script to launch cctv

is_running() {
  pgrep -lf ".[ /]$1( |\$)"
}

app_path="$HOME/pyprojs/cctv"
cctv_launch="imgcap.py"

cd $app_path
source env/bin/activate

# launch cctv tasks
if is_running "$cctv_launch" >/dev/null; then
    echo "$cctv_launch already running"
    else
        echo "launching $cctv_launch"
        python3 $cctv_launch >> /dev/null 2>&1 & 
fi
