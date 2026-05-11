from flask import Flask, render_template_string, request
import hashlib

app = Flask(__name__)

# --- قاعدة بيانات العملة (محاكاة لنظامك) ---
# ملاحظة: في النسخة المتقدمة سنقوم بربط هذا بملف ghon.py الأصلي
total_supply = 20000000
accounts = {
    'FROZEN_VAULT': 10000000,
    'PUZZLE_REWARDS': 5000000,
}
# إضافة الـ 1000 محفظة تلقائياً ليتعرف عليها الموقع
for i in range(1, 1001):
    wallet_id = hashlib.sha256(f"secret_key_{i}".encode()).hexdigest()[:16]
    accounts[f"Private_Wallet_{wallet_id}"] = 5000

# --- تصميم الواجهة (HTML) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>GHON-BIT | Explorer</title>
    <style>
        body { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; text-align: center; padding-top: 50px; }
        .box { border: 1px solid #00ff00; display: inline-block; padding: 20px; box-shadow: 0 0 15px #00ff00; }
        input { background: #111; color: #0f0; border: 1px solid #0f0; padding: 10px; width: 300px; text-align: center; }
        button { background: #00ff00; color: #000; border: none; padding: 10px 20px; cursor: pointer; font-weight: bold; }
        .result { margin-top: 20px; font-size: 1.2em; color: #fff; }
    </style>
</head>
<body>
    <div class="box">
        <h1>🌑 GHON-BIT NETWORK 🌑</h1>
        <p>ENTER WALLET ADDRESS TO CHECK BALANCE</p>
        <form method="POST">
            <input type="text" name="address" placeholder="0x... or Wallet Name" required><br><br>
            <button type="submit">QUERY LEDGER</button>
        </form>
        
        {% if balance is not none %}
        <div class="result">
            <p>Address: {{ address }}</p>
            <p>Balance: <span style="color:#00ff00;">{{ balance }} $GHN</span></p>
        </div>
        {% elif error %}
        <div class="result" style="color: red;">{{ error }}</div>
        {% endif %}
    </div>
    <p style="margin-top: 50px; opacity: 0.5;">Status: Node_Irbid_Online | Encryption: AES-256</p>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    balance = None
    address = None
    error = None
    if request.method == 'POST':
        address = request.form.get('address')
        if address in accounts:
            balance = accounts[address]
        else:
            error = "⚠️ Address not found in the Ghost Ledger."
    return render_template_string(HTML_TEMPLATE, balance=balance, address=address, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

