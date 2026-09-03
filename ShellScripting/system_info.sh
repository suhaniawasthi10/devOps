#!/bin/bash

# Store system information in variables
current_date=$(date)
hostname=$(hostname)
username=$(whoami)

# Take directory name from the user
read -p "Enter directory name: " directory

# Create the directory
mkdir -p "$directory"

# Create a file inside the directory
file="$directory/processes.txt"
touch "$file"

# Display system information
echo "===== System Information ====="
echo "Current Date: $current_date"
echo "Hostname: $hostname"
echo "Username: $username"

echo ""
echo "===== Disk Usage ====="
df -h

echo ""
echo "===== Running Processes ====="
ps

# Store running processes in the file
ps > "$file"

echo ""
echo "Running processes have been saved to $file"