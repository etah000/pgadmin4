#!/usr/bin/env bash
echo "build server"
cd ./server
pip3 install virtualenv
virtualenv -p python3.9 .venv
source .venv/bin/activate
pip install -r requirements.txt
pyinstaller app/app.py --onefile --hidden-import pkg_resources.py2_warn --hidden-import cmath
cp ./dist/app ../client/extraResources
cd ..
echo "build client"
cd ./client
npm install
npm run electron:build

