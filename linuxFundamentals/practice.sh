#!/usr/bin/env bash
# Use an Ubuntu VM with systemd for the user/log tasks in README.md.
set -euo pipefail
lab_dir=$(mktemp -d "${TMPDIR:-/tmp}/devops-linux.XXXXXX")
cd "$lab_dir"
pwd
printf 'Hello students\n' > original.txt
ln original.txt hardlink.txt
ln -s original.txt softlink.txt
ls -li original.txt hardlink.txt softlink.txt
rm original.txt
cat hardlink.txt
if [ -e softlink.txt ]; then echo 'Unexpected: soft link still resolves'; exit 1; fi
ls -l softlink.txt
rm hardlink.txt softlink.txt
mkdir files
touch files/demo.txt
cp files/demo.txt files/copy.txt
mv files/copy.txt files/renamed.txt
chmod 600 files/renamed.txt
ls -l files
find files -type f
whoami
df -h
ps
printf 'Practice directory retained for inspection: %s\n' "$lab_dir"
