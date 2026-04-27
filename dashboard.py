from flask import Flask, render_template_string, jsonify
import json
from shield import AiClassifiedShield

app = Flask(__name__)
shield = AiClassifiedShield()

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ai-classy | Neural Audit</title>
    <style>
        :root { --neon-blue: #00e5ff; --bg-dark: #050505; --card-bg: rgba(20, 20, 20, 0.9); }
        body { background: var(--bg-dark); color: white; font-family: sans-serif; margin: 0; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }
        .pulse-bg { position: fixed; top: 50%; left: 50%; width: 400px; height: 400px; background: radial-gradient(circle, rgba(0,229,255,0.1) 0%, transparent 70%); transform: translate(-50%, -50%); animation: pulse 4s infinite; z-index: -1; }
        @keyframes pulse { 0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.3; } 50% { transform: translate(-50%, -50%) scale(1.4); opacity: 0.6; } }
        .container { width: 90%; max-width: 500px; padding-top: 50px; text-align: center; }
        .total-score { font-size: 110px; font-weight: 800; color: var(--neon-blue); filter: drop-shadow(0 0 15px rgba(0,229,255,0.5)); margin: 0; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 30px; width: 100%; }
        .card { background: var(--card-bg); border: 1px solid rgba(0,229,255,0.2); padding: 20px; border-radius: 20px; backdrop-filter: blur(10px); cursor: pointer; transition: 0.2s; text-align: left; }
        .card:active { transform: scale(0.95); border-color: var(--neon-blue); }
        .card h3 { margin: 0; font-size: 10px; text-transform: uppercase; letter-spacing: 2px; color: #888; }
        .score { font-size: 26px; font-weight: bold; color: var(--neon-blue); margin-top: 5px; }
        
        #modal-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); z-index: 100; }
        .modal { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 85%; max-width: 400px; background: #111; border: 1px solid var(--neon-blue); border-radius: 20px; padding: 25px; box-shadow: 0 0 30px rgba(0,229,255,0.2); }
        .tabs { display: flex; justify-content: space-between; margin: 20px 0; border-bottom: 1px solid #222; }
        .tab { padding: 10px; color: #555; cursor: pointer; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; }
        .tab.active { color: var(--neon-blue); border-bottom: 2px solid var(--neon-blue); }
        .view-area { font-family: 'Courier New', monospace; font-size: 13px; max-height: 300px; overflow-y: auto; text-align: left; }
        .pass { color: var(--neon-blue); }
        .fail { color: #ff3d00; }
    </style>
</head>
<body>
    <div class="pulse-bg"></div>
    <div class="container">
        <h3 style="letter-spacing: 3px; font-weight: 200; color: #555;">AUDIT RADIUS</h3>
        <div class="total-score">{{ total }}</div>
        <div class="grid">
            {% for q in ['operability', 'regulatory', 'context', 'velocity'] %}
            {% set results, q_score = shield.get_results(q) %}
            <div class="card" data-quadrant="{{ q }}" data-json='{{ results | tojson | safe }}' onclick="openModal(this)">
                <h3>{{ q }}</h3>
                <div class="score">{{ q_score }}/9</div>
            </div>
            {% endfor %}
        </div>
    </div>

    <div id="modal-overlay" onclick="closeModal()">
        <div class="modal" onclick="event.stopPropagation()">
            <h2 id="m-title" style="margin:0; color:var(--neon-blue); font-weight: 200; letter-spacing: 2px;"></h2>
            <div class="tabs">
                <div id="t-trace" class="tab active" onclick="setView('trace')">Trace</div>
                <div id="t-manifest" class="tab" onclick="setView('manifest')">Files</div>
                <div id="t-data" class="tab" onclick="setView('data')">Raw</div>
            </div>
            <div id="m-content" class="view-area"></div>
            <button onclick="closeModal()" style="margin-top:20px; width:100%; background:none; border:1px solid #333; color:#666; padding:10px; border-radius:10px; cursor:pointer;">DISMISS</button>
        </div>
    </div>

    <script>
        let activeData = [];
        function openModal(el) {
            activeData = JSON.parse(el.getAttribute('data-json'));
            document.getElementById('m-title').innerText = el.getAttribute('data-quadrant').toUpperCase();
            document.getElementById('modal-overlay').style.display = 'block';
            setView('trace');
        }
        function closeModal() { document.getElementById('modal-overlay').style.display = 'none'; }
        function setView(v) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.getElementById('t-' + v).classList.add('active');
            const target = document.getElementById('m-content');
            if(v === 'trace') target.innerHTML = activeData.map(i => `<div>[${i.status == 'PASS' ? '<span class="pass">✔</span>' : '<span class="fail">✘</span>'}] ${i.name}</div>`).join('');
            if(v === 'manifest') target.innerHTML = activeData.map(i => `<div>• ${i.name}</div>`).join('');
            if(v === 'data') target.innerHTML = `<pre style="color:#00ff41; font-size:10px;">${JSON.stringify(activeData, null, 2)}</pre>`;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML, total=shield.get_total_score(), shield=shield)

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
