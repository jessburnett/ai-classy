from flask import Flask, render_template_string
from shield import AiClassifiedShield

app = Flask(__name__)
shield = AiClassifiedShield()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>ai-classy | Sovereign Dashboard</title>
    <style>
        body { background: #0a0a0a; color: #00e5ff; font-family: sans-serif; text-align: center; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; padding: 20px; }
        .card { border: 1px solid #222; padding: 20px; border-radius: 15px; background: #111; }
        .score-big { font-size: 80px; text-shadow: 0 0 20px #00e5ff; }
    </style>
</head>
<body>
    <h1>TOTAL SCORE</h1>
    <div class="score-big">{{ total }}</div>
    <div class="grid">
        {% for q in ['operability', 'regulatory', 'context', 'velocity'] %}
        <div class="card">
            <h3>{{ q.upper() }}</h3>
            <p>{{ shield.get_results(q)[1] }}/9</p>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML, total=shield.get_total_score(), shield=shield)

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
