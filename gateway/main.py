# 기존 코드 전체 주석 처리
# from fastapi import FastAPI, Request
# import httpx
# from fastapi.responses import JSONResponse
# 
# app = FastAPI()
# 
# SERVICE_MAP = {
#     "chatbot": "http://localhost:8001",
#     "report-auth": "http://localhost:8002",
#     "cbam-data": "http://localhost:8003",
#     "cbam-calc": "http://localhost:8004",
#     "cbam-settings": "http://localhost:8005",
# }
# 
# @app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
# async def proxy(service: str, path: str, request: Request):
#     if service not in SERVICE_MAP:
#         return JSONResponse(status_code=404, content={"error": "Service not found"})
#     url = f"{SERVICE_MAP[service]}/{path}"
#     async with httpx.AsyncClient() as client:
#         response = await client.request(
#             request.method,
#             url,
#             headers=dict(request.headers),
#             content=await request.body()
#         )
#     return JSONResponse(status_code=response.status_code, content=response.json()) 

from fastapi import APIRouter, FastAPI

# FP 스타일로 gateway_router 생성

gateway_router = APIRouter()

@gateway_router.get("/sample-get")
def sample_get():
    """GET 샘플 엔드포인트"""
    return {"message": "GET 요청 성공"}

@gateway_router.post("/sample-post")
def sample_post():
    """POST 샘플 엔드포인트"""
    return {"message": "POST 요청 성공"}

@gateway_router.put("/sample-put")
def sample_put():
    """PUT 샘플 엔드포인트"""
    return {"message": "PUT 요청 성공"}

@gateway_router.delete("/sample-delete")
def sample_delete():
    """DELETE 샘플 엔드포인트"""
    return {"message": "DELETE 요청 성공"}

# FastAPI 앱에 라우터 등록
app = FastAPI()
app.include_router(gateway_router, prefix="/gateway") 
