# Shell Scripting - System Information Script

## About the Task

I created a shell script that shows some basic information about the system like the current date, hostname, username, disk usage and running processes.

The script also takes a directory name from the user, creates that directory, creates a file inside it and stores the running processes in that file.

## Script

The script is saved as `system_info.sh`.

```bash
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
```

## Commands Used

### `mkdir`

I used `mkdir` to create the directory entered by the user.

```bash
mkdir -p "$directory"
```

### `touch`

I used `touch` to create the `processes.txt` file inside the directory.

```bash
touch "$file"
```

### `echo`

I used `echo` to print the system information on the terminal.

```bash
echo "Current Date: $current_date"
```

### `df`

`df` is used to check the disk usage of the system.

```bash
df -h
```

### `ps`

`ps` is used to display the currently running processes.

```bash
ps
```

### `read -p`

I used `read -p` to take the directory name as input from the user.

```bash
read -p "Enter directory name: " directory
```

### Variables

I used variables to store values like the date, hostname and username so that they can be used later in the script.

```bash
current_date=$(date)
hostname=$(hostname)
username=$(whoami)
```

### `>` Output Redirection

I used `>` to save the output of the `ps` command into `processes.txt`.

```bash
ps > "$file"
```

This means that instead of only displaying the process information on the terminal, it is also stored in the file.

## How I Ran the Script

First, I gave execute permission to the script:

```bash
chmod +x system_info.sh
```

Then I ran it using:

```bash
./system_info.sh
```

The script asked me for a directory name:

```text
Enter directory name: devops_data
```

## Output

The script displayed the following information:

```text
===== System Information =====
Current Date: [your actual output]
Hostname: [your actual output]
Username: [your actual output]

===== Disk Usage =====
[your actual df -h output]

===== Running Processes =====
[your actual ps output]

Running processes have been saved to devops_data/processes.txt
```

## Checking the Created Files

After running the script, I checked the directory using:

```bash
ls
```

The directory created was:

```text
devops_data
```

I then checked the file inside it:

```bash
ls devops_data
```

Output:

```text
processes.txt
```

To check the process information stored in the file:

```bash
cat devops_data/processes.txt
```

This showed the output of the `ps` command.

## Project Structure

```text
ShellScripting/
├── system_info.sh
├── README.md
└── devops_data/
    └── processes.txt
```