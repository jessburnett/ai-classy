from flask import Flask, render_template_string
import base64, json
from shield import AiClassifiedShield

app = Flask(__name__)
shield = AiClassifiedShield()

def get_persona(s):
    return {"rank": "Omniscient Void-Walker", "icon": "👽", "color": "#00e5ff"} if s >= 36 else {"rank": "Cerebral Starchild", "icon": "✨", "color": "#7000ff"}

@app.template_filter('b64encode')
def b64encode_filter(s):
    return base64.b64encode(json.dumps(s).encode()).decode()

MAIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ai-classy | Neural Audit</title>
    <style>
        :root { --neon: #00e5ff; --bg: #050505; --glass: rgba(30, 30, 30, 0.8); }
        body { background: var(--bg); color: white; font-family: sans-serif; margin: 0; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }
        .container { width: 90%; max-width: 450px; padding: 40px 0; text-align: center; }
        .total-score { font-size: 110px; font-weight: 900; color: var(--neon); filter: drop-shadow(0 0 20px rgba(0,229,255,0.4)); margin: 0; }
        .persona-box { background: var(--glass); border: 1px solid rgba(0,229,255,0.2); border-radius: 30px; padding: 25px; margin: 25px 0; backdrop-filter: blur(15px); cursor: pointer; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; width: 100%; }
        .card { background: var(--glass); border: 1px solid rgba(255,255,255,0.05); padding: 20px; border-radius: 20px; cursor: pointer; text-align: left; }
        .card .val { font-size: 24px; font-weight: bold; color: var(--neon); }
        #modal { display: none; position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.95); z-index: 100; backdrop-filter: blur(15px); }
        .m-box { position: absolute; top:50%; left:50%; transform:translate(-50%,-50%); width: 88%; max-width:400px; background:#0a0a0a; border: 1px solid #222; border-radius:30px; padding:30px; }
        .tabs { display: flex; justify-content: space-around; margin: 20px 0; border-bottom: 1px solid #1a1a1a; }
        .tab { padding: 12px; font-size: 11px; color: #444; cursor: pointer; font-weight: bold; }
        .tab.active { color: var(--neon); border-bottom: 2px solid var(--neon); }
        .view-area { font-family: monospace; font-size: 11px; height: 260px; overflow-y: auto; text-align: left; color: #999; }
        .pass { color: var(--neon); } .fail { color: #ff3d00; }
        .close-btn { margin-top: 20px; width: 100%; padding: 15px; background: #111; border: 1px solid #222; color: #555; border-radius: 15px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h3 style="letter-spacing: 5px; color: #444;">NEURAL AUDIT</h3>
        <div class="total-score">{{ total }}</div>
        <div class="persona-box" onclick="window.location.href='/governance'">
            <div style="font-size: 55px;">{{ persona.icon }}</div>
            <div style="font-size: 18px; font-weight: bold; color: {{ persona.color }};">{{ persona.rank }}</div>
            <p style="font-size: 10px; color: #555; text-transform: uppercase;">AIGA Strategic Map</p>
        </div>
        <div class="grid">
            {% for q in ['operability', 'regulatory', 'context', 'velocity'] %}
            {% set results, q_score = shield.get_results(q) %}
            <div class="card" onclick="openM('{{ q }}', '{{ results | b64encode }}')">
                <h3 style="font-size:10px; color:#555; text-transform:uppercase; margin:0;">{{ q }}</h3>
                <div class="val">{{ q_score }}/9</div>
            </div>
            {% endfor %}
        </div>
    </div>
    <div id="modal" onclick="closeM()">
        <div class="m-box" onclick="event.stopPropagation()">
            <h2 id="mt" style="color:var(--neon); font-weight: 200; margin:0;"></h2>
            <div class="tabs">
                <div id="t-trace" class="tab active" onclick="setV('trace')">TRACE</div>
                <div id="t-files" class="tab" onclick="setV('files')">FILES</div>
                <div id="t-data" class="tab" onclick="setV('data')">JSON</div>
            </div>
            <div id="mc" class="view-area"></div>
            <button class="close-btn" onclick="closeM()">DISMISS</button>
        </div>
    </div>
    <script>
        let currentData = [];
        function openM(title, b64) {
            currentData = JSON.parse(atob(b64));
            document.getElementById('mt').innerText = title.toUpperCase();
            document.getElementById('modal').style.display = 'block';
            setV('trace');
        }
        function closeM() { document.getElementById('modal').style.display = 'none'; }
        function setV(v) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.getElementById('t-' + v).classList.add('active');
            const area = document.getElementById('mc');
            if(v === 'trace') area.innerHTML = currentData.map(i => `<div>[${i.status == 'PASS' ? '<span class="pass">✔</span>' : '<span class="fail">✘</span>'}] ${i.name}</div>`).join('');
            if(v === 'files') area.innerHTML = currentData.map(i => `<div>• ${i.name}</div>`).join('');
            if(v === 'data') area.innerHTML = `<pre style="color:var(--neon); font-size:10px;">${JSON.stringify(currentData, null, 2)}</pre>`;
        }
    </script>
</body>
</html>
"""

GOV_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SAIG Sovereign HUD</title>
    <style>
        :root { --neon: #00e5ff; --bg: #050505; }
        body { background: var(--bg); color: white; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; min-height: 100vh; margin: 0; }
        .header { width: 90%; max-width: 400px; padding: 30px 0; }
        .back-btn { color: var(--neon); background: none; border: 1px solid var(--neon); padding: 8px 15px; border-radius: 12px; cursor: pointer; font-size: 10px; margin-bottom: 25px; }
        .tier { background: rgba(255,255,255,0.03); border-left: 4px solid var(--neon); padding: 25px; border-radius: 0 20px 20px 0; margin-bottom: 15px; width: 85%; max-width: 380px; position: relative; }
        .tier-header { font-size: 10px; color: var(--neon); text-transform: uppercase; letter-spacing: 2px; }
        .tier-title { font-size: 18px; font-weight: bold; margin: 5px 0; }
        .tier-desc { font-size: 12px; color: #777; line-height: 1.5; }
        .stat-orb { position: absolute; right: 20px; top: 50%; transform: translateY(-50%); width: 45px; height: 45px; border: 1px solid var(--neon); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: var(--neon); }
        footer { margin-top: 40px; font-size: 10px; color: #333; width: 85%; max-width: 380px; border-top: 1px solid #111; padding-top: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <button class="back-btn" onclick="window.location.href='/'">← BACK TO CORE</button>
        <h1 style="font-weight: 200; font-size: 32px; margin:0;">SAIG <span style="color:var(--neon)">HUD</span></h1>
    </div>
    <div class="tier">
        <div class="tier-header">Environmental Layer</div>
        <div class="tier-title">Global Hard Law</div>
        <div class="tier-desc">Alignment with Colorado SB 24-205 and global standards.</div>
        <div class="stat-orb">36</div>
    </div>
    <div class="tier" style="border-left-color: #7000ff;">
        <div class="tier-header" style="color:#7000ff">Organizational Layer</div>
        <div class="tier-title">Strategic Alignment</div>
        <div class="tier-desc">Strategic alignment at the "neck" of the AIGA Hourglass.</div>
        <div class="stat-orb" style="border-color:#7000ff; color:#7000ff;">A+</div>
    </div>
    <div class="tier" style="border-left-color: #39ff14;">
        <div class="tier-header" style="color:#39ff14">AI System Layer</div>
        <div class="tier-title">Operational Excellence</div>
        <div class="tier-desc">System design and technical operational logic.</div>
        <div class="stat-orb" style="border-color:#39ff14; color:#39ff14;">S</div>
    </div>
    <footer>
        ENV: TERMUX ON MOBILE<br>
        DEVELOPER: Jess Burnett<br>
        LOCATION: Arvada, CO
    </footer>
</body>
</html>
"""

@app.route('/')
def home():
    s = shield.get_total_score()
    return render_template_string(MAIN_HTML, total=s, shield=shield, persona=get_persona(s))

@app.route('/governance')
def governance():
    return render_template_string(GOV_HTML)

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
