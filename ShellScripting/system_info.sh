#!/usr/bin/env bash
set -euo pipefail
current_date=$(date)
machine_name=$(hostname)
username=$(whoami)
read -r -p "Enter directory name: " directory
if [ -z "$directory" ]; then echo 'Directory name must not be empty.' >&2; exit 1; fi
mkdir -p -- "$directory"
file="$directory/processes.txt"
touch -- "$file"
echo '===== System Information ====='
echo "Current Date: $current_date"
echo "Hostname: $machine_name"
echo "Username: $username"
echo '===== Disk Usage ====='
df -h
echo '===== Running Processes ====='
ps
ps > "$file"
echo "Running processes have been saved to $file"
