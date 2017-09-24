#!/bin/bash
# Script to start server

pip install -r requirements.txt

python populate.py

python DyReTra/DyReTra.py