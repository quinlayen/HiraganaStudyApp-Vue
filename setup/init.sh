#!/bin/bash
################
# Run this file first
################m

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Installing Python 3..."
    # Install Python 3 (modify this line if you have a specific way to install Python)
    brew install python3
else
    # Check if the installed Python version is at least 3.8
    PYTHON_VERSION=$(python3 -V | cut -d ' ' -f 2)
    REQUIRED_VERSION="3.8"
    if [[ $(echo -e "$PYTHON_VERSION\n$REQUIRED_VERSION" | sort -V | head -n1) == $REQUIRED_VERSION ]]; then
        echo "Python 3.8 or newer is already installed."
    else
        echo "Python 3 is installed but version is less than 3.8. Installing a newer version..."
        # Install a newer version of Python 3 (modify this line if you have a specific way to install Python)
        brew install python3
    fi
fi

# Create and activate a virtual environment called sandbox
echo "Creating and activating virtual environment 'sandbox'..."
python3 -m venv sandbox
source sandbox/bin/activate

# Install dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Change permission of run.sh to 700
echo "Changing permission of run.sh to 700..."
chmod 700 run.sh

# Create a directory called log if it doesn't exist
echo "Creating a 'log' directory..."
mkdir -p log

echo "Script completed."
