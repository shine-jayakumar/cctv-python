#!/bin/bash

# cctv_tasks.sh
# script to launch cctv tasks

is_running() {
  pgrep -lf ".[ /]$1( |\$)"
}

app_path="$HOME/pyprojs/cctv"
cctv_tasks="cctv_tasks.py"

cd $app_path
source env/bin/activate

# launch cctv tasks
if is_running "$cctv_tasks" >/dev/null; then
    echo "$cctv_tasks already running"
    else
        echo "launching $cctv_tasks"
        python3 $cctv_tasks >> /dev/null 2>&1 & 
fi
