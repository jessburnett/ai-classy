# ai-classy: Agentic Orchestration Recipes
setup:
    @echo "Initializing ai-classy environment..."
    pip install -r requirements.txt
    chmod +x reproduce.sh
    @echo "✅ Setup Complete."
audit:
    python shield.py
dashboard:
    python dashboard.py
