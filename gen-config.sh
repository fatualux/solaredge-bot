#!/bin/bash

# Define CONFIG_FILE variable
CONFIG_FILE="secrets.sh"

# Prompt the user for their tokens and site id
echo -n "Enter your Solaredge's token: "
read -r SITE_TOKEN
echo -n "Enter your Solaredge's site id: "
read -r SITE_ID
echo -n "Enter your Telegram bot token: "
read -r BOT_TOKEN

# Write the configuration to the config.py file
cat <<EOL > $CONFIG_FILE
BASEURL = '$BASEURL'
SITE_TOKEN = '$SITE_TOKEN'
BOT_TOKEN = '$BOT_TOKEN'
SITE_ID = '$SITE_ID'
EOL

echo "Configuration written to $CONFIG_FILE"
