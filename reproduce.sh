#!/bin/bash
# ai-classy: Deterministic Environment Recovery
echo "--- REPRODUCE: ai-classy ---"
uname -a
pip install --upgrade pip
pip install -r requirements.txt
python shield.py
echo "--- REPRODUCTION COMPLETE ---"
