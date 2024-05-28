#!/bin/bash

# Read configuration from venv.cfg file
source ./venv.cfg

# verify if config.py exists and create it if not
config_file_exists() {
  if [ -f $CONFIG_FILE ]; then
    echo "Config file found."
  else
    echo "Config file not found. Creating..."
    echo -n "Enter your Solaredge's token: "
    read -r site_token
    echo -n "Enter your Solaredge's site id: "
    read -r site_id
    echo -n "Enter your Telegram bot token: "
    read -r bot_token
    echo "BASEURL = '$BASEURL'" > $CONFIG_FILE
    echo "bot_token = '$bot_token'" > $CONFIG_FILE
    echo "site_token = '$site_token'" >> $CONFIG_FILE
    echo "site_id = '$site_id'" >> $CONFIG_FILE
    echo "Config file created."
  fi
}


deactivate_venv() {
  echo "Deactivating virtual environment..."
  deactivate
  echo "Virtual environment deactivated."
}

# Trap Ctrl+C and call deactivate_venv function
trap deactivate_venv SIGINT

dependency_check() {
  if command -v virtualenv &> /dev/null; then
    echo "vOk, virtualenv package is installed on your system."
    export VENV_COMMAND=virtualenv
  else
    echo "A suitable Python virtual environment is not installed on your system."
    echo "Please install virtualenv and try again."
    echo "Aborting..."
    exit
  fi
}

venv_create() {
  # Remove venv directory if it exists
  if [ -d "$WORKDIR" ]; then
    rm -rf $WORKDIR
    echo "Old virtual environment deleted."
  fi
  echo "Starting Python Virtual Environment setup..."
  echo ""
  echo "Python Virtual Environment not found. Creating..."
  $VENV_COMMAND $WORKDIR
  echo ""
  echo "Python virtual environment created."
  echo ""
}

copy_files() {
  echo "Copying requirements..."
  cp $REQUIREMENTS_FILE $WORKDIR
  echo "Copying application file..."
  cp $APP_FILE $WORKDIR
  echo "Copying config file..."
  cp $CONFIG_FILE $WORKDIR
  echo "Copying modules..."
  cp -r $MODULES_DIR $WORKDIR

  echo ""
  echo "Done."
}

venv_activate() {
  echo "Activating virtual environment..."
  source $WORKDIR/bin/activate
  echo ""
}

install_req() {
  echo "Installing requirements..."
  pip install --upgrade pip && pip install -r $REQUIREMENTS_FILE
  echo ""
  echo "Done."
}

starting_app() {
  echo "Starting application..."
  echo ""
  python $WORKDIR/$APP_FILE
}

config_file_exists
dependency_check
venv_create
copy_files
venv_activate
install_req
starting_app
