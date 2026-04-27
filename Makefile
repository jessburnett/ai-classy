# ai-classy Legacy Orchestration
.PHONY: setup audit dashboard

setup:
pip install -r requirements.txt
chmod +x reproduce.sh

audit:
python shield.py

dashboard:
python dashboard.py
