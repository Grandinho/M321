#!/bin/bash
 
run_curls() {
    local source=$1
    local dest_upload=$2
    local ip=$3
 
    curl -XPOST http://192.168.100.$ip:2019/download --data "{\"source\": \"$source\", \"destination\": \"$dest_upload\"}" &
    curl -XPOST http://192.168.100.$ip:2019/upload --data "{\"source\": \"$dest_upload\", \"destination\": \"$source\"}" &
}
 
if [ -z "$1" ]; then
    echo "Usage: $0 <source-station>"
    exit 1
fi
 
stations=("Station 10-A" "Station 11-A" "Station 12-A" "Station 13-A" "Station 14-A" "Station 15-A" "Station 16-A" "Station 17-A")
source_station=$1
ip=$2
 
while true; do
  for destination_station in "${stations[@]}"; do
    if [[ "$destination_station" != "$source_station" ]]; then
            run_curls "$source_station" "$destination_station" "$ip"
    fi
    done
    wait
    sleep 0.1
done