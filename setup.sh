#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

echo -e "\033[1;36m==> Starting pinout-cli global system installation...\033[0m"

# 1. Ensure pinout.py is executable locally
chmod +x pinout.py

# 2. Safely symlink the script to the local binary folder using sudo
echo -e "\033[1;33m==> Creating global symlink at /usr/local/bin/pinout (requires sudo privileges)...\033[0m"
sudo ln -sf "$(pwd)/pinout.py" /usr/local/bin/pinout

echo -e "\033[1;32m==> Installation complete! You can now use the 'pinout' command anywhere.\033[0m"
echo -e "Try running: \033[1mpinout esp32-s3\033[0m"
