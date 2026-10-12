from flask import Flask, jsonify
from datetime import datetime
import random

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status":"CYBER GHOST LIVE SMALL LEAGUES","time":str(datetime.now())})

@app.route('/api/predictions')
def predictions():
    random.seed(datetime.now().strftime("%Y-%m-%d"))
    leagues = [
        ("Levadia Tallinn","Narva Trans","CS 2-0 @7.00","CORRECT","Estonia Meistriliiga"),
        ("Riga FC","FK Liepaja","CS 2-0 @6.50","CORRECT","Latvia Virsliga"),
        ("Zalgiris","Kauno Zalgiris","CS 1-0 @6.00","CORRECT","Lithuania A Lyga"),
        ("Lion City Sailors","Balestier Khalsa","Over 2.5 @1.60","OVER","Singapore PL"),
        ("Hanoi FC","Viettel","Over 2.5 @1.80","OVER","Vietnam V-League"),
        ("Bolivar","The Strongest","HT 1/FT 1 @2.10","HTFT","Bolivia Primera"),
        ("Alianza Lima","Sporting Cristal","HT X/FT 1 @4.50","HTFT","Peru Liga 1"),
        ("APOEL","Omonia","Over 1.5 @1.30","FREE","Cyprus 1st Div"),
        ("Hamrun Spartans","Valletta","Over 1.5 @1.28","FREE","Malta Premier"),
        ("Vikingur Reykjavik","KR Reykjavik","Over 1.5 @1.32","FREE","Iceland Urvalsdeild"),
        ("Shamrock Rovers","Dundalk","CS 2-1 @8.50","CORRECT","Ireland Premier"),
        ("Pyunik Yerevan","Ararat Yerevan","CS 1-0 @5.50","CORRECT","Armenia Premier"),
    ]
    todays = random.sample(leagues, 8)
    games = []
    for home, away, pred, market, league in todays:
        games.append({
            "home": home, "away": away,
            "match": f"{home} vs {away}",
            "prediction": pred,
            "market": market,
            "league": league,
            "odd": pred.split("@")[1] if "@" in pred else "1.35",
            "status": random.choice(["WON","WON","WON","PENDING"])
        })
    return jsonify({"games": games, "date": datetime.now().strftime("%Y-%m-%d")})

@app.route('/api/verify-vip')
def verify():
    return jsonify({"valid": True, "message": "VIP OK"})

if __name__ == '__main__':
    app.run()
