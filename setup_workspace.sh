#!/bin/bash
#
# Copyright (c) 2025
#           Thomas Bömer (thomas.bömer@tu-dortmund.de)
#           Nico Koltermann (nico.koltermann@tu-dortmund.de) 
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

SAMPLE_DIR="./docs/samples" 

# Check if the file exists in the destination directory
if [ -e "./.env" ]; then
    echo "Check .env file ok - file exists."
else
    echo "!!! NO .env FILE available." 
    echo "COPY SAMPLE..."
    echo "Please check the README!"
    # Copy the file to the destination directory with the new name
    cp "$SAMPLE_DIR/sample_env" "./.env"
    exit 1
fi

source .env

if [ "$EOH_PROBLEM" = "multibay_reshuffle" ]; then
    if [ -e "./eoh_experiment/exp_1.json" ]; then
        echo "Check eoh_experiment file ok - file exists."
    else
        cp "$SAMPLE_DIR/sample_experiment" "./eoh_experiment/exp_1.json"
        echo "!!! NO EXPERIEMNT FILE available." 
        echo "COPY SAMPLE..."
        echo "Please check the README!"
    fi
fi

ZIP_FILE="./instances/instances.zip"  # Change to your actual ZIP file
EXTRACT_FOLDER="./instances/instances"  # Folder where files should be extracted

# Check if the extracted folder exists
if [ -d "$EXTRACT_FOLDER" ]; then
    echo "Folder already exists: $EXTRACT_FOLDER"
else
    echo "Folder does not exist. Extracting ZIP file..."
    if [ -f "$ZIP_FILE" ]; then
        mkdir -p "$EXTRACT_FOLDER"  # Create the folder
        unzip "$ZIP_FILE" -d "./instances/"  # Extract ZIP into the folder
        echo "Extraction complete: Files are now in $EXTRACT_FOLDER."
    else
        echo "ZIP file not found: $ZIP_FILE"
        exit 1
    fi
fi
