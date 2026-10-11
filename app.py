from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import json, os, hashlib, random, string

app = Flask(__name__)
DB = "db.json"

def load():
    if not os.path.exists(DB):
        return {"codes": {}, "today": {}}
    return json.load(open(DB))

def save(d):
    json.dump(d, open(DB,"w"), indent=2)

def ghost(match):
    key=match.lower()
    seed=int(hashlib.md5(key.encode()).hexdigest(),16)%(2**32)
    rng=random.Random(seed)
    ft_h, ft_a = rng.choice([(1,0),(2,0),(2,1),(1,1),(0,1),(0,2)])
    conf = rng.randint(60,95)
    res = "HOME WIN" if ft_h>ft_a else "AWAY WIN" if ft_a>ft_h else "DRAW"
    return {"match":match.upper(),"ft":f"{ft_h}-{ft_a}","result":f"{res} - {conf}% SURE","conf":conf}

@app.route("/activate")
def activate():
    code=request.args.get("code","").upper()
    db=load()
    c=db["codes"].get(code)
    if not c:
        return jsonify({"error":"Invalid code"})
    if c.get("used")==False:
        c["expires"]=(datetime.now()+timedelta(days=c["days"])).isoformat()
        c["used"]=True
        save(db)
    exp=datetime.fromisoformat(c["expires"])
    if datetime.now()>exp:
        return jsonify({"valid":False,"expired":True})
    return jsonify({"valid":True,"plan":c["plan"],"expires":c["expires"]})

@app.route("/gen")
def gen():
    if request.args.get("secret")!="GHOST2026":
        return "Wrong secret"
    plan=request.args.get("plan")
    days=int(request.args.get("days"))
    code=f"{plan.upper()[:4]}-{days}D-{''.join(random.choices(string.ascii_uppercase+string.digits,k=4))}"
    db=load()
    db["codes"][code]={"plan":plan,"days":days,"used":False,"expires":None}
    save(db)
    return jsonify({"code":code,"plan":plan,"days":days})

@app.route("/today/<plan>")
def today(plan):
    matches=["Man City vs Arsenal","Barcelona vs Real Madrid","Bayern vs Dortmund"]
    picks=[ghost(m) for m in matches]
    return jsonify(picks)

@app.route("/")
def home():
    return "☠️ CYBER GHOST API Running"

app.run(host="0.0.0.0", port=10000)
