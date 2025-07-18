from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
import os

app = FastAPI()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URI)
db = client[os.getenv("MONGODB_DB", "ESG")]

# precursors 예시
@app.get("/cbam-data/precursors/")
async def get_precursors(search: str = Query("", alias="search")):
    query = {"$or": [
        {"품목": {"$regex": search, "$options": "i"}},
        {"cn코드": {"$regex": search, "$options": "i"}}
    ]} if search else {}
    materials = await db["material"].find(query).limit(50).to_list(50)
    mapped = [{
        "_id": str(m["_id"]),
        "name": m.get("품목"),
        "directFactor": m.get("직접"),
        "indirectFactor": m.get("간접"),
        "cnCode": str(m.get("cn코드")),
    } for m in materials]
    return {"precursors": mapped}

# materials 예시
@app.get("/cbam-data/materials/")
async def get_materials(search: str = Query("", alias="search")):
    query = {"투입물_혹은_산출물": {"$regex": search, "$options": "i"}} if search else {}
    mats = await db["Raw"].find(query).limit(50).to_list(50)
    mapped = [{
        "품목": m.get("투입물_혹은_산출물", ""),
        "품목En": m.get("투입물_혹은_산출물_영어", ""),
        "직접": m.get("배출_계수_(t_co₂/t)_)"),
        "cn코드": m.get("cn코드", ""),
        "cn코드1": m.get("cn코드1", ""),
        "cn코드2": m.get("cn코드2", ""),
    } for m in mats]
    return {"materials": mapped}

# fuels 예시
@app.get("/cbam-data/fuels/")
async def get_fuels(search: str = Query("", alias="search")):
    def escape_regex(text):
        import re
        return re.escape(text)
    query = {"연료_유형_설명": {"$regex": escape_regex(search), "$options": "i"}} if search else {}
    fuels = await db["Fuel"].find(query).limit(50).to_list(50)
    mapped = [{
        "연료명": f.get("연료_유형_설명", ""),
        "연료명En": f.get("연료_유형_설명_영어", ""),
        "배출계수": float(f.get("배출계수\n(tco₂/tj)", 0)),
        "순발열량": float(f.get("순발열량\n(tj/gg)", 0)),
    } for f in fuels]
    return {"fuels": mapped}

# hscode 예시
@app.get("/cbam-data/hscode/")
async def get_hscode(hs: str = Query("", alias="hs"), page: int = Query(1, alias="page")):
    PAGE_SIZE = 5
    query = {}
    if hs:
        hs_num = int(hs) if hs.isdigit() else None
        if hs_num is not None:
            min_hs = hs_num * 10 ** (6 - len(hs))
            max_hs = min_hs + 10 ** (6 - len(hs)) - 1
            query = {"$or": [
                {"hs_코드": {"$gte": min_hs, "$lte": max_hs}},
                {"cn_검증용": {"$gte": min_hs, "$lte": max_hs}}
            ]}
    total = await db["HSCODE"].count_documents(query)
    docs = await db["HSCODE"].find(query).sort("hs_코드", 1).skip((page - 1) * PAGE_SIZE).limit(PAGE_SIZE).to_list(PAGE_SIZE)
    return {"results": docs, "total": total, "page": page, "pageSize": PAGE_SIZE, "query": query.get("$or", [{}])[0] if "$or" in query else {}}

# country 예시
@app.get("/cbam-data/country/")
async def get_country():
    countries = await db["Country"].find().to_list(50)
    return {"country": countries}

# get-cbam-price 예시
@app.get("/cbam-data/get-cbam-price/")
async def get_cbam_price():
    # 실제 가격 계산 로직 필요
    return {"price": 0}

# my-precursors 예시
@app.get("/cbam-data/my-precursors/")
async def get_my_precursors(userId: str = Query("demo", alias="userId")):
    precursors = await db["precursor"].find({"userId": userId}).sort("createdAt", -1).to_list(50)
    return precursors

@app.delete("/cbam-data/my-precursors/")
async def delete_my_precursor(id: str, userId: str = Query("demo", alias="userId")):
    from bson import ObjectId
    result = await db["precursor"].delete_one({"_id": ObjectId(id), "userId": userId})
    return {"ok": result.deleted_count == 1}

# precursor-materials
@app.get("/cbam-data/precursor-materials/")
async def get_precursor_materials(search: str = Query("", alias="search")):
    query = {"품목_(cn기준)": {"$regex": search, "$options": "i"}} if search else {}
    mats = await db["HSCODE"].find(query).to_list(50)
    mapped = [{
        "HS_코드": m.get("hs_코드"),
        "품목": m.get("품목_(cn기준)"),
        "품목영문": m.get("품목_(cn기준_영문)"),
        "직접": m.get("직접"),
        "간접": m.get("간접"),
    } for m in mats]
    return {"materials": mapped} 