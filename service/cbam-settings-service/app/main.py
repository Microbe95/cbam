from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
import os

app = FastAPI()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URI)
db = client[os.getenv("MONGODB_DB", "ESG")]

@app.get("/cbam-settings/tax/")
async def get_tax():
    taxData = await db["Tax"].find_one({})
    if not taxData:
        return JSONResponse(status_code=404, content={"error": "Tax data not found"})
    return {
        "kerosene": taxData.get("등유"),
        "butane": taxData.get("부탄"),
        "naturalGas": taxData.get("천연가스"),
        "propane": taxData.get("프로판"),
        "heavyOil": taxData.get("중유")
    }

@app.get("/cbam-settings/tax-e/")
async def get_tax_e():
    taxData = await db["Tax_E"].find_one({})
    if not taxData:
        return JSONResponse(status_code=404, content={"error": "Tax_E data not found"})
    return {"total": taxData.get("합계")}

@app.get("/cbam-settings/tax-t/{id}/")
async def get_tax_t(id: str):
    # 실제 교통세 데이터 반환 로직 필요 (예시)
    return {"tax_t": 0, "id": id}

@app.get("/cbam-settings/kets/")
async def get_kets():
    ketsData = await db["Kets"].find_one({})
    if not ketsData:
        return JSONResponse(status_code=404, content={"error": "K-ETS data not found"})
    return {"yearlyAverage": ketsData.get("k-ets연간 평균값")}

@app.get("/cbam-settings/company/")
async def get_company():
    # 실제 회사 데이터 반환 로직 필요 (예시)
    return {"company": {}}

@app.get("/cbam-settings/ETS/")
async def get_ets():
    collection = db["ETS"]
    today = os.getenv("ETS_DATE_OVERRIDE") or None
    docs = await collection.find({}, {"projection": {"date": 1, "auction_price_€/tco2": 1}}).to_list(100)
    if not docs:
        return JSONResponse(status_code=404, content={"error": "No ETS data found"})
    from datetime import datetime
    today_dt = datetime.now() if not today else datetime.strptime(today, "%Y-%m-%d")
    closest = min(docs, key=lambda d: abs(datetime.strptime(d["date"], "%Y-%m-%d") - today_dt))
    return {"price": closest.get("auction_price_€/tco2"), "date": closest.get("date")} 