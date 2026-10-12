from flask import Flask, jsonify
from datetime import datetime
import random

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status":"SMALL LEAGUES LIVE","time":str(datetime.now())})

@app.route('/api/predictions')
def predictions():
    random.seed(int(datetime.now().strftime("%Y%m%d")))
    leagues = [
        ("Levadia Tallinn","Narva Trans","CS 2-0 @7.00","CORRECT","Estonia Meistriliiga","7.00"),
        ("Riga FC","FK Liepaja","CS 2-0 @6.50","CORRECT","Latvia Virsliga","6.50"),
        ("Zalgiris","Kauno Zalgiris","CS 1-0 @6.00","CORRECT","Lithuania A Lyga","6.00"),
        ("Shamrock Rovers","Dundalk","CS 2-1 @8.50","CORRECT","Ireland Premier","8.50"),
        ("Pyunik Yerevan","Ararat Yerevan","CS 1-0 @5.50","CORRECT","Armenia Premier","5.50"),
        ("Lion City Sailors","Balestier Khalsa","Over 2.5 @1.60","OVER","Singapore PL","1.60"),
        ("Hanoi FC","Viettel","Over 2.5 @1.80","OVER","Vietnam V-League","1.80"),
        ("Bolivar","The Strongest","HT 1/FT 1 @2.10","HTFT","Bolivia Primera","2.10"),
        ("APOEL","Omonia","Over 1.5 @1.30","FREE","Cyprus 1st Div","1.30"),
        ("Hamrun Spartans","Valletta","Over 1.5 @1.28","FREE","Malta Premier","1.28"),
        ("Vikingur Reykjavik","KR Reykjavik","Over 1.5 @1.32","FREE","Iceland Urvalsdeild","1.32"),
    ]
    todays = random.sample(leagues, 8)
    games = []
    for home, away, pred, market, league, odd in todays:
        games.append({
            "home": home, "away": away,
            "prediction": pred, "market": market,
            "league": league, "odd": odd, "odds": odd,
            "status": "WON" if market=="FREE" else random.choice(["WON","WON","PENDING"])
        })
    return jsonify({"predictions": games, "games": games, "date": datetime.now().strftime("%Y-%m-%d")})

@app.route('/api/verify-vip')
def verify():
    return jsonify({"valid": True})

if __name__ == '__main__':
    app.run()
