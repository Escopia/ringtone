#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
echo "Starting Audio Distribution Portal Test Server..."
python test_local.py
