from flask import Flask, render_template_string, jsonify
from shield import AiClassifiedShield
import os
import json

app = Flask(__name__)
shield = AiClassifiedShield()

# Expanded metric mapping for the "Full Pass/Fail" report
METRIC_DETAILS = {
    "operability": ["justfile", "Makefile", "package.json", "reproduce.sh", "venv", "requirements.txt"],
    "context": ["CLAUDE.md", "ARCHITECTURE.md", "docs/adr", "README.md"],
    "regulatory": ["SB24-205_NOTICE.md", "IDENTITY.json", "AIBOM.json", "LICENSE"],
    "velocity": ["AGENT_POLICY.md", ".agent/state.json", ".github/workflows"]
}

def get_active_agent():
    # Check AIBOM or environment for active agent identity
    if os.path.exists("AIBOM.json"):
        try:
            with open("AIBOM.json", "r") as f:
                data = json.load(f)
                return data.get("foundation_models", [{}])[0].get("model_name", "Unknown Agent")
        except: pass
    return "Local Instance"

@app.route('/api/drilldown/<quadrant>')
def api_drilldown(quadrant):
    files = METRIC_DETAILS.get(quadrant.lower(), [])
    report = []
    for f in files:
        exists = os.path.exists(f) or os.path.isdir(f)
        report.append({
            "name": f,
            "status": "PASS" if exists else "FAIL",
            "color": "text-cyan-400" if exists else "text-rose-500"
        })
    return jsonify({"quadrant": quadrant, "report": report})

@app.route('/')
def home():
    results = shield.run_36_point_audit()
    total = sum(results.values())
    agent = get_active_agent()
    return render_template_string(HTML_TEMPLATE, scores=results, total=total, agent=agent)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        :root { --ai-glow: #00f2ff; }
        body { background: #020203; color: #fff; font-family: 'Inter', sans-serif; }
        .ai-core {
            width: 160px; height: 160px;
            background: radial-gradient(circle, var(--ai-glow) 0%, transparent 75%);
            filter: blur(25px); border-radius: 50%;
            animation: pulse {{ 5 - (total/10) }}s infinite ease-in-out;
            opacity: 0.5;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 0.3; }
            50% { transform: scale(1.2); opacity: 0.7; }
        }
        .glass { background: rgba(20, 20, 25, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.05); }
        .modal-show { opacity: 1 !important; pointer-events: auto !important; transform: translateY(0) !important; }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center p-6 space-y-6">

    <header class="w-full max-w-md flex justify-between items-center px-2">
        <div class="text-[10px] font-black tracking-[0.4em] text-cyan-500 uppercase">ai-classy</div>
        <div class="px-3 py-1 bg-cyan-500/10 border border-cyan-500/20 rounded-full text-[9px] font-bold text-cyan-400 uppercase tracking-tighter">
            Agent: {{ agent }}
        </div>
    </header>

    <div class="relative flex items-center justify-center py-8">
        <div class="ai-core"></div>
        <div class="absolute text-center">
            <div class="text-6xl font-black tracking-tighter">{{ total }}</div>
            <div class="text-[10px] uppercase tracking-widest text-cyan-500/50 font-bold">Total Score</div>
        </div>
    </div>

    <div class="grid grid-cols-2 gap-4 w-full max-w-md">
        {% for key, val in scores.items() %}
        <button onclick="drillDown('{{ key }}')" class="glass p-5 rounded-2xl text-left active:scale-95 transition-all">
            <div class="text-[9px] uppercase tracking-widest text-gray-500 mb-1">{{ key }}</div>
            <div class="text-2xl font-bold italic">{{ val }}/9</div>
            <div class="mt-3 h-1 w-full bg-white/5 rounded-full overflow-hidden">
                <div class="h-full bg-cyan-500" style="width: {{ (val/9)*100 }}%"></div>
            </div>
        </button>
        {% endfor %}
    </div>

    <div id="modal" class="fixed inset-0 z-50 flex items-end md:items-center justify-center p-4 opacity-0 pointer-events-none transition-all duration-300 transform translate-y-10">
        <div class="glass w-full max-w-sm p-8 rounded-[2rem] shadow-2xl border-cyan-500/10">
            <h2 id="modalTitle" class="text-xl font-black italic tracking-tighter mb-6 text-cyan-400 uppercase"></h2>
            <div id="modalContent" class="space-y-3"></div>
            <button onclick="closeModal()" class="mt-8 w-full py-4 rounded-xl bg-cyan-500 text-black font-black text-xs tracking-widest uppercase">Dismiss Trace</button>
        </div>
    </div>

    <script>
        async function drillDown(quadrant) {
            const res = await fetch(`/api/drilldown/${quadrant}`);
            const data = await res.json();
            document.getElementById('modalTitle').innerText = data.quadrant + ' Trace';
            let html = '';
            data.report.forEach(item => {
                html += `<div class="flex justify-between items-center text-xs py-1">
                            <span class="opacity-50 font-mono tracking-tighter">${item.name}</span>
                            <span class="${item.color} font-black">${item.status}</span>
                         </div>`;
            });
            document.getElementById('modalContent').innerHTML = html;
            document.getElementById('modal').classList.add('modal-show');
        }
        function closeModal() { document.getElementById('modal').classList.remove('modal-show'); }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)

