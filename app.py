from flask import Flask,request,jsonify
from flask_cors import CORS
from datetime import datetime,timedelta
import random,json,os
app=Flask(__name__)
CORS(app)
VIP_FILE="vip_codes.json"
ADMIN_SECRET="CYBER_ADMIN_2024"
def load_db():
 if os.path.exists(VIP_FILE):
  try:
   with open(VIP_FILE) as f: return json.load(f)
  except: pass
 return {"CYBER2024":{"market":"ALL","expires":"2030-12-31T23:59:59","type":"lifetime","days":9999}}
def save_db(d):
 try:
  with open(VIP_FILE,'w') as f: json.dump(d,f)
 except: pass
vip_db=load_db()
def get_preds():
 return [{"home":"Man City","away":"Arsenal","prediction":"Over 2.5","odds":"1.85","market":"OVER"},{"home":"Barcelona","away":"Real Madrid","prediction":"BTTS Yes","odds":"1.75","market":"BTTS"},{"home":"Bayern","away":"Dortmund","prediction":"HT/FT 1/1","odds":"4.50","market":"HTFT"},{"home":"PSG","away":"Marseille","prediction":"Home Win","odds":"2.10","market":"WINS"},{"home":"Inter","away":"AC Milan","prediction":"Draw","odds":"3.40","market":"DRAWS"},{"home":"Liverpool","away":"Chelsea","prediction":"Correct Score 2-1","odds":"12.00","market":"CORRECT"}]
@app.route('/')
def home(): return jsonify(status="Cyber Ghost API Live",whatsapp="+237 6 83 67 05 78")
@app.route('/api/predictions')
def preds(): return jsonify(predictions=get_preds())
@app.route('/api/verify-vip')
def verify():
 code=request.args.get('code','').upper()
 d=vip_db.get(code)
 if not d: return jsonify(valid=False)
 exp=datetime.fromisoformat(d['expires'])
 return jsonify(valid=datetime.now()<=exp,expired=datetime.now()>exp,market=d['market'],expires=d['expires'],type=d['type'])
@app.route('/api/generate-vip',methods=['POST'])
def gen():
 j=request.get_json()
 if not j or j.get('secret')!=ADMIN_SECRET: return jsonify(error="Forbidden"),403
 m=j.get('market','HTFT').upper()
 dur=j.get('duration','1week')
 days={"1week":7,"2weeks":14,"1month":30}.get(dur,7)
 code=f"{m}-{dur[:4].upper()}-{random.randint(1000,9999)}"
 exp=datetime.now()+timedelta(days=days)
 vip_db[code]={"market":m,"expires":exp.isoformat(),"type":dur,"days":days}
 save_db(vip_db)
 return jsonify(code=code,market=m,duration=dur,days=days,expires=exp.isoformat())
if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.environ.get('PORT',10000)))
