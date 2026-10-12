from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import random, json, os

app = Flask(__name__)
CORS(app)

DB = {"CYBER2024": {"market": "ALL", "expires": "2030-12-31T23:59:59", "type": "lifetime"}}

@app.route('/')
def home():
    return jsonify({"status": "Cyber Ghost API Live", "whatsapp": "+237 6 83 67 05 78"})

@app.route('/api/predictions')
def preds():
    games = [
        {"home": "Man City", "away": "Arsenal", "prediction": "Over 2.5", "odds": "1.85", "market": "OVER"},
        {"home": "Barcelona", "away": "Real Madrid", "prediction": "BTTS Yes", "odds": "1.75", "market": "BTTS"},
        {"home": "Bayern", "away": "Dortmund", "prediction": "HT/FT 1/1", "odds": "4.50", "market": "HTFT"},
    ]
    return jsonify({"predictions": games})

@app.route('/api/verify-vip')
def verify():
    code = request.args.get('code', '').upper()
    data = DB.get(code)
    if not data:
        return jsonify({"valid": False})
    exp = datetime.fromisoformat(data["expires"])
    ok = datetime.now() <= exp
    return jsonify({"valid": ok, "market": data["market"], "expires": data["expires"]})

@app.route('/api/generate-vip', methods=['POST'])
def gen():
    j = request.get_json()
    if not j or j.get('secret')!= 'CYBER_ADMIN_2024':
        return jsonify({"error": "Forbidden"}), 403
    market = j.get('market', 'HTFT')
    code = f"{market}-{random.randint(1000,9999)}"
    exp = datetime.now() + timedelta(days=7)
    DB[code] = {"market": market, "expires": exp.isoformat()}
    return jsonify({"code": code, "market": market, "expires": exp.isoformat()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
