from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
import os

app = FastAPI()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URI)
db = client[os.getenv("MONGODB_DB", "ESG")]

@app.post("/cbam-calc/calculate/fuel/")
async def calculate_fuel(request: Request):
    data = await request.json()
    fuel_name = data.get("fuel_name")
    fuel_amount = data.get("fuel_amount")
    if not fuel_name or fuel_amount is None:
        return JSONResponse(status_code=400, content={"error": "fuel_name과 fuel_amount를 모두 입력하세요."})
    fuelCol = db["Fuel"]
    fuelDoc = await fuelCol.find_one({"연료_유형_설명": {"$regex": f"^{fuel_name.strip()}$", "$options": "i"}})
    if not fuelDoc:
        return JSONResponse(status_code=404, content={"error": "해당 연료명을 찾을 수 없습니다."})
    emissionFactor = float(fuelDoc.get("배출계수\n(tco₂/tj)", 0))
    netCalorificValue = float(fuelDoc.get("순발열량\n(tj/gg)", 0))
    if emissionFactor == 0 or netCalorificValue == 0:
        return JSONResponse(status_code=500, content={"error": "DB에 배출계수 또는 순발열량 값이 올바르지 않습니다."})
    emission = fuel_amount * netCalorificValue * emissionFactor * 1e-3
    return {
        "emission": round(emission, 6),
        "fuel_name": fuelDoc["연료_유형_설명"],
        "emissionFactor": emissionFactor,
        "netCalorificValue": netCalorificValue
    }

@app.post("/cbam-calc/calculate/material/")
async def calculate_material(request: Request):
    data = await request.json()
    material_name = data.get("material_name")
    material_amount = data.get("material_amount")
    if not material_name or material_amount is None:
        return JSONResponse(status_code=400, content={"error": "material_name과 material_amount를 모두 입력하세요."})
    matCol = db["material"]
    matDoc = await matCol.find_one({"품목": {"$regex": f"^{material_name}$", "$options": "i"}})
    if not matDoc or matDoc.get("직접") is None:
        return JSONResponse(status_code=404, content={"error": "해당 원료명을 찾을 수 없거나 직접배출계수가 없습니다."})
    emissionFactor = float(matDoc["직접"])
    emission = material_amount * emissionFactor * 1.0
    return {"emission": round(emission, 6)} 