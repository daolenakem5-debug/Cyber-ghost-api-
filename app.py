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
    leagues=[
        ("Levadia Tallinn","Narva Trans","CS 2-0 @7.00","CORRECT","Estonia","7.00"),
        ("Riga FC","Liepaja","CS 2-0 @6.50","CORRECT","Latvia","6.50"),
        ("Zalgiris","Kauno Zalgiris","CS 1-0 @6.00","CORRECT","Lithuania","6.00"),
        ("Shamrock Rovers","Dundalk","CS 2-1 @8.50","CORRECT","Ireland","8.50"),
        ("APOEL","Omonia","Over 1.5 @1.30","FREE","Cyprus","1.30"),
        ("Hamrun","Valletta","Over 1.5 @1.28","FREE","Malta","1.28"),
    ]
    todays=random.sample(leagues,5)
    games=[]
    for h,a,p,m,l,o in todays:
        games.append({"home":h,"away":a,"prediction":p,"market":m,"league":l,"odd":o,"odds":o,"status":"WON" if m=="FREE" else "PENDING"})
    return jsonify({"predictions":games,"games":games})

@app.route('/api/verify-vip')
def verify():
    return jsonify({"valid":True})

if __name__=='__main__':
    app.run()
