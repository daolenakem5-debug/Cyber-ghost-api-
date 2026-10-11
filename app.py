from flask import Flask, request, jsonify
import random, string, hashlib, datetime, math

app = Flask(__name__)
SECRET = "GHOST2026"
codes_db = {}

# YOUR PRICING
PRICING = {
    "HTFT": {"1W": 5000, "2W": 8000, "1M": 15000, "min_odds": 4, "max_odds": 10, "days": {"1W":7,"2W":14,"1M":30}},
    "OVER": {"1W": 3000, "2W": 5000, "1M": 9500, "min_odds": 3, "max_odds": 10, "days": {"1W":7,"2W":14,"1M":30}},
    "CORRECT": {"1W": 10000, "2W": 18000, "1M": 30000, "min_odds": 10, "max_odds": 50, "days": {"1W":7,"2W":14,"1M":30}},
    "ALL": {"1M": 50000, "min_odds": 3, "max_odds": 50, "days": {"1M":30}}
}

WHATSAPP = "+237 6 83 67 05 78"
WHATSAPP_LINK = "https://wa.me/237683670578"

def gen_code(plan, duration):
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"{plan}-{duration}-{rand}"

# GHOST V6.7 VARIETY ENGINE - AUTO DAILY
def pmf(k,lam): return (lam**k*math.exp(-lam))/math.factorial(k)

def predict_match(home,away):
    key=home.lower()+away.lower()+str(datetime.date.today())
    seed=int(hashlib.md5(key.encode()).hexdigest(),16)%999999
    random.seed(seed)
    def pw(n):
        h=int(hashlib.md5(n.lower().encode()).hexdigest(),16)
        r=random.Random(h)
        a=r.uniform(0.75,1.8)
        d=r.uniform(0.7,1.4)
        return a,d
    ha,hd=pw(home); aa,ad=pw(away)
    lh=min(3.8,max(0.4,1.2*ha*ad)); la=min(3.8,max(0.4,1.1*aa*hd))
    prob={}; scores=[]
    for i in range(7):
        for j in range(7):
            pr=pmf(i,lh)*pmf(j,la)
            if i==j: pr*=0.4
            prob[(i,j)]=pr
            scores.append((pr,i,j))
    scores.sort(reverse=True)
    top_no_draw=[(p,i,j) for p,i,j in scores if i!=j][:8]
    weights=[p for p,_,_ in top_no_draw]
    chosen=random.choices(top_no_draw, weights=weights, k=1)[0]
    fh,fa=chosen[1],chosen[2]
    if (fh==1 and fa==0) or (fh==0 and fa==1):
        if random.random()>0.6:
            if lh>la: fh,fa=random.choice([2,3]), random.choice([0,1])
            else: fh,fa=random.choice([0,1]), random.choice([2,3])
    tot=fh+fa
    hh=max(0, fh-random.randint(0,1)) if fh>0 else 0
    ha2=max(0, fa-random.randint(0,1)) if fa>0 else 0
    htft=f"{'H' if hh>ha2 else 'A' if ha2>hh else 'H' if lh>=la else 'A'}{'H' if fh>fa else 'A'}"
    o25 = 1 - sum(v for (i,j),v in prob.items() if i+j<=2)
    btts = 1 - (sum(prob[(0,j)] for j in range(7))+sum(prob[(i,0)] for i in range(7))-prob[(0,0)])
    return {"home":home,"away":away,"ft":f"{fh}-{fa}","ht":f"{hh}-{ha2}","htft":htft,"over25": round(o25*100,1), "btts": round(btts*100,1), "total":tot}

# Daily fixtures - auto (you can edit this list or connect to API later)
TODAY_FIXTURES = [
    ("Real Madrid","Barcelona"), ("Man City","Arsenal"), ("Bayern","Dortmund"),
    ("PSG","Marseille"), ("Inter","AC Milan"), ("Liverpool","Chelsea"),
    ("Atletico","Sevilla"), ("Ajax","PSV"), ("Benfica","Porto"), ("Galatasaray","Fenerbahce")
]

@app.route('/')
def home():
    return jsonify({
        "status": "CYBER GHOST PREDICTION API Live",
        "whatsapp": WHATSAPP,
        "whatsapp_link": WHATSAPP_LINK,
        "pricing_XAF": PRICING,
        "how_to_buy": f"Contact WhatsApp {WHATSAPP_LINK}?text=I%20want%20VIP to pay via MoMo, then receive code"
    })

@app.route('/pricing')
def pricing():
    return jsonify(PRICING)

@app.route('/gen')
def generate():
    if request.args.get('secret')!= SECRET: return "Wrong secret", 403
    plan = request.args.get('plan','OVER').upper()
    duration = request.args.get('duration','1W').upper()
    if plan not in PRICING or duration not in PRICING[plan]["days"]:
        return jsonify({"error":"Use plan=HTFT/OVER/CORRECT/ALL & duration=1W/2W/1M"}), 400
    days = PRICING[plan]["days"][duration]
    price = PRICING[plan][duration]
    code = gen_code(plan,duration)
    expire = datetime.datetime.now() + datetime.timedelta(days=days)
    codes_db[code] = {"plan": plan, "duration": duration, "expire": expire}
    return jsonify({"code": code, "plan": plan, "duration": duration, "price_XAF": price, "days": days, "expires": expire.strftime("%Y-%m-%d")})

@app.route('/activate')
def activate():
    code = request.args.get('code','').strip().upper()
    info = codes_db.get(code)
    if not info: return jsonify({"valid": False, "reason": "invalid code", "whatsapp": WHATSAPP_LINK})
    if datetime.datetime.now() > info["expire"]:
        return jsonify({"valid": False, "reason": "expired", "whatsapp": WHATSAPP_LINK})
    return jsonify({"valid": True, "plan": info["plan"], "duration": info["duration"], "expire": info["expire"].strftime("%Y-%m-%d")})

@app.route('/daily')
def daily():
    code = request.args.get('code','').strip().upper()
    req_plan = request.args.get('plan','OVER').upper()
    # Free check
    if req_plan=="FREE":
        data=[predict_match(h,a) for h,a in TODAY_FIXTURES[:3]]
        return jsonify({"date": str(datetime.date.today()), "plan":"FREE", "predictions": data})
    info = codes_db.get(code)
    if not info: return jsonify({"valid": False, "need_code": True, "whatsapp": WHATSAPP_LINK}), 403
    if datetime.datetime.now() > info["expire"]: return jsonify({"valid": False, "expired": True, "whatsapp": WHATSAPP_LINK}), 403
    if info["plan"]!="ALL" and info["plan"]!=req_plan: return jsonify({"valid": False, "wrong_plan": True, "your_plan": info["plan"]}), 403

    preds = [predict_match(h,a) for h,a in TODAY_FIXTURES]
    # Filter by odds logic per plan
    if req_plan=="OVER":
        result=[{"match":f"{p['home']} vs {p['away']}", "tip": f"Over 2.5 ({p['over25']}%)", "odds": round(random.uniform(3,10),2)} for p in preds]
    elif req_plan=="HTFT":
        result=[{"match":f"{p['home']} vs {p['away']}", "tip": f"HT/FT {p['htft']}", "ft":p['ft'], "odds": round(random.uniform(4,10),2)} for p in preds]
    elif req_plan=="CORRECT":
        result=[{"match":f"{p['home']} vs {p['away']}", "tip": f"Correct Score {p['ft']}", "ht":p['ht'], "odds": round(random.uniform(10,50),2)} for p in preds]
    else: # ALL
        result=preds
    return jsonify({"date": str(datetime.date.today()), "plan": req_plan, "vip_code": code, "predictions": result, "whatsapp": WHATSAPP_LINK})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
