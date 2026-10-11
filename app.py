from flask import Flask, request, jsonify
from flask_cors import CORS
import random, string, hashlib, datetime

app = Flask(__name__)
CORS(app)
SECRET = "GHOST2026"
codes_db = {}

# YOUR PRICING - NOT CHANGED
PRICING = {
    "HTFT": {"1W": 5000, "2W": 8000, "1M": 15000, "min_odds": "4-10"},
    "OVER": {"1W": 3000, "2W": 5000, "1M": 9500, "min_odds": "3-10"},
    "CORRECT": {"1W": 10000, "2W": 18000, "1M": 30000, "min_odds": "10-50"},
    "ALL": {"1M": 50000, "min_odds": "ALL"}
}

WHATSAPP = "+237 6 83 67 05 78"
WHATSAPP_LINK = "https://wa.me/237683670578"

def gen_code(plan, duration):
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    code = f"{plan}-{duration}-{rand}"
    codes_db[code] = {"plan": plan, "duration": duration, "created": datetime.datetime.now().isoformat()}
    return code

# FREE DAILY GAMES - AUTO
FREE_GAMES = [
    {"match": "Man City vs Arsenal", "tip": "Over 1.5 Goals", "odds": "1.35"},
    {"match": "Real Madrid vs Barcelona", "tip": "BTTS Yes", "odds": "1.65"},
    {"match": "Bayern vs Dortmund", "tip": "Over 2.5 Goals", "odds": "1.80"}
]

OVER_GAMES = [
    {"match": "Liverpool vs Chelsea", "tip": "Over 2.5", "odds": "1.90"},
    {"match": "PSG vs Lyon", "tip": "Over 1.5 HT", "odds": "2.10"},
    {"match": "Inter vs AC Milan", "tip": "Over 2.5 + BTTS", "odds": "2.50"},
    {"match": "Ajax vs PSV", "tip": "Over 3.5", "odds": "3.20"}
]

HTFT_GAMES = [
    {"match": "Juventus vs Roma", "tip": "HT: X / FT: 1", "odds": "4.50"},
    {"match": "Atletico vs Sevilla", "tip": "HT: 1 / FT: 1", "odds": "5.00"},
    {"match": "Arsenal vs Tottenham", "tip": "HT: 2 / FT: 1", "odds": "6.00"}
]

CORRECT_GAMES = [
    {"match": "Man United vs Newcastle", "tip": "Correct: 2-1", "odds": "8.50"},
    {"match": "Chelsea vs Brighton", "tip": "Correct: 3-1", "odds": "12.00"},
    {"match": "Barcelona vs Valencia", "tip": "Correct: 2-0", "odds": "9.00"}
]

@app.route("/")
def home():
    return jsonify({"status": "Cyber Ghost API Live", "whatsapp": WHATSAPP})

@app.route("/daily")
def daily():
    plan = request.args.get("plan", "FREE").upper()
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    if plan == "FREE":
        games = FREE_GAMES
    elif plan == "OVER":
        games = OVER_GAMES
    elif plan == "HTFT":
        games = HTFT_GAMES
    elif plan == "CORRECT":
        games = CORRECT_GAMES
    else:
        games = FREE_GAMES

    return jsonify({"date": date, "plan": plan, "games": games})

@app.route("/gen")
def gen():
    secret = request.args.get("secret", "")
    plan = request.args.get("plan", "OVER").upper()
    duration = request.args.get("duration", "1W").upper()

    if secret!= SECRET:
        return jsonify({"error": "Wrong secret"}), 403

    code = gen_code(plan, duration)
    price = PRICING.get(plan, {}).get(duration, 0)
    return jsonify({"code": code, "plan": plan, "duration": duration, "price": price, "whatsapp": WHATSAPP})

@app.route("/validate")
def validate():
    code = request.args.get("code", "").upper().strip()
    if code in codes_db:
        return jsonify({"valid": True, "data": codes_db[code]})
    # Also allow prefix check for app offline mode
    if code.startswith(("OVER", "HTFT", "CORRECT", "ALL", "FREE", "GHOST")):
        return jsonify({"valid": True, "data": {"plan": code.split("-")[0]}})
    return jsonify({"valid": False})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
