#!/bin/bash
################
# Run this file first
################m

confirm_installation() {
    while true; do
        read -p "Do you wish to install Python 3? (y/n) " yn
        case $yn in
            [Yy]* ) break;;
            [Nn]* ) echo "Python installation aborted."; exit;;
            * ) echo "Please answer yes or no.";;
        esac
    done
}

# Check if Python 3.8 or higher is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed."
    confirm_installation
    echo "Installing Python 3..."
    brew install python3
else
   
    PYTHON_VERSION=$(python3 -V | cut -d ' ' -f 2)
    REQUIRED_VERSION="3.8"
    if [[ $(echo -e "$PYTHON_VERSION\n$REQUIRED_VERSION" | sort -V | head -n1) == $REQUIRED_VERSION ]]; then
        echo "Python 3.8 or newer is already installed."
    else
        echo "Python 3 is installed but version is less than 3.8."
        confirm_installation
        echo "Installing a newer version..."
        brew install python3
    fi
fi

# Create and activate a virtual environment for Python
echo "Creating and activating virtual environment 'venv'..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

deactivate

echo "Changing permission of run.sh to 700..."
chmod 700 run.sh


echo "Creating a 'log' directory..."
mkdir -p log

echo `basename $0 completed successfully`

./run.sh