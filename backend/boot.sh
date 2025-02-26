#!/bin/bash
source "$(find . -type f -name activate | grep .)"
python3 app.py

# Windows script
# Scripts\activate
# python app.py