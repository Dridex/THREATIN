#!/bin/bash

cd threat-agent
./install-TA.sh

while true; do
    read -p "Do you want to install the web agent?[y/n] " yn
    case $yn in
        [Yy]* ) cd ../web-agent; ./install-WA.sh; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer y or n.";;
    esac
done
