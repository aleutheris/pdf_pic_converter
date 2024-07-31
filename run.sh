#!/bin/bash

PROJECT_DIRECTORY="pdf_pic_converter"
FILES_DIRECTORY="$PROJECT_DIRECTORY/files"
IMAGE_NAME="pdf_pic_converter:latest"


docker --version
if [ $? -ne 0 ]; then
    echo "Docker is not installed. Please install Docker before running this script."
    exit 1
fi

if [ -d "$PROJECT_DIRECTORY" ]; then
    echo "The directory $PROJECT_DIRECTORY already exists. Please delete it before running this script."
    exit 1
fi

mkdir -p "$PROJECT_DIRECTORY"
mkdir -p "$FILES_DIRECTORY"
cd "$PROJECT_DIRECTORY"

wget https://raw.githubusercontent.com/aleutheris/pdf_pic_converter/main/main.py
wget https://raw.githubusercontent.com/aleutheris/pdf_pic_converter/main/Dockerfile
wget https://raw.githubusercontent.com/aleutheris/pdf_pic_converter/main/requirements.txt


python3 -m venv .venv

source .venv/bin/activate

pip3 install -r requirements.txt

python3 main.py

deactivate

cd ..
rm -rf "$PROJECT_DIRECTORY"
