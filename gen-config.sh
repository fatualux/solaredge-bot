#!/bin/bash

# Define BASEURL variable
BASEURL="https://monitoringapi.solaredge.com"

# Define CONFIG_FILE variable
CONFIG_FILE="config.py"

# Prompt the user for their tokens and site id
echo -n "Enter your Solaredge's token: "
read -r site_token
echo -n "Enter your Solaredge's site id: "
read -r site_id
echo -n "Enter your Telegram bot token: "
read -r bot_token

# Write the configuration to the config.py file
cat <<EOL > $CONFIG_FILE
BASEURL = '$BASEURL'
site_token = '$site_token'
bot_token = '$bot_token'
site_id = '$site_id'
EOL

echo "Configuration written to $CONFIG_FILE"
