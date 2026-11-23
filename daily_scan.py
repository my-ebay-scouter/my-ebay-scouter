import os,json,base64,urllib.parse,urllib.request,urllib.error
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parent
C=json.loads((R/"config.json").read_text(encoding="utf-8"))
def call(url,headers,data=None,method=None):
 req=urllib.request.Request(url,data=data,headers=headers,method=method)
 with urllib.request.urlopen(req,timeout=30) as x:return json.loads(x.read().decode())
def token():
 basic=base64.b64encode((os.environ["EBAY_CLIENT_ID"]+":"+os.environ["EBAY_CLIENT_SECRET"]).encode()).decode()
 body=urllib.parse.urlencode({"grant_type":"client_credentials","scope":"https://api.ebay.com/oauth/api_scope"}).encode()
 return call("https://api.ebay.com/identity/v1/oauth2/token",{"Authorization":"Basic "+basic,"Content-Type":"application/x-www-form-urlencoded"},body,"POST")["access_token"]
def main():
 t=token();items=[];warnings=[]
 for cat in C["categories"]:
  cid=str(cat.get("ebay_category_id","")).strip()
  if not cid:
   warnings.append(cat["name"]+": eBay category ID未設定");continue
  q=urllib.parse.urlencode({"category_id":cid,"metric_name":"BEST_SELLING","limit":C["daily_limit_per_category"]})
  try:
   data=call("https://api.ebay.com/buy/marketing/v1_beta/merchandised_product?"+q,{"Authorization":"Bearer "+t,"X-EBAY-C-MARKETPLACE-ID":C["marketplace_id"]})
   for p in data.get("merchandisedProducts",[]):
    title=p.get("title") or str(p.get("epid") or "商品名未取得")
    enc=urllib.parse.quote(title)
    items.append({"genre":cat["name"],"title":title,"epid":p.get("epid"),"price":p.get("price"),"source":"eBay Marketing API BEST_SELLING",
     "mercari":"https://www.mercari.com/jp/search/?keyword="+enc,
     "yahoo_flea":"https://paypayfleamarket.yahoo.co.jp/search/"+enc,
     "yahoo_auction":"https://auctions.yahoo.co.jp/search/search?p="+enc,
     "status":"国内価格・状態の確認が必要"})
  except urllib.error.HTTPError as e:warnings.append(f'{cat["name"]}: HTTP {e.code} '+e.read().decode(errors="replace")[:300])
  except Exception as e:warnings.append(f'{cat["name"]}: {type(e).__name__}: {e}')
 out={"generated_at":datetime.now(timezone.utc).isoformat(),"budget_yen":C["max_purchase_yen"],"target_profit_yen":C["target_profit_yen"],"items":items,"warnings":warnings,
 "limitations":["BEST_SELLINGは人気商品シグナルであり、実売履歴や販売率そのものではありません。","Marketplace Insightsの販売履歴APIは限定提供です。","国内フリマは検索リンクのみ。自動スクレイピングは行いません。","国内仕入れ価格・商品状態を確認するまで利益は確定できません。"]}
 (R/"data/daily_report.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
 print("report items:",len(items),"warnings:",len(warnings))
if __name__=="__main__":main()
