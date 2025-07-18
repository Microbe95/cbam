from fastapi import APIRouter, Request
from ...domain.customer.command.controller import CustomerCommandController
import asyncio

# client_router 생성
client_router = APIRouter()

# CustomerCommandController 인스턴스 생성
controller = CustomerCommandController()

@client_router.post("/customer/create")
async def create_customer(request: Request):
    data = await request.json()
    result = await controller.create_customer(**data)
    return {"message": result}

@client_router.put("/customer/update")
async def update_customer(request: Request):
    data = await request.json()
    result = await controller.update_customer(**data)
    return {"message": result}

@client_router.delete("/customer/delete")
async def delete_customer(request: Request):
    data = await request.json()
    result = await controller.delete_customer(**data)
    return {"message": result}

# 기존 샘플 엔드포인트
@client_router.get("/sample-get")
def client_sample_get():
    """GET 샘플 엔드포인트 (client)"""
    return {"message": "client GET 요청 성공"}

@client_router.post("/sample-post")
def client_sample_post():
    """POST 샘플 엔드포인트 (client)"""
    return {"message": "client POST 요청 성공"}

@client_router.put("/sample-put")
def client_sample_put():
    """PUT 샘플 엔드포인트 (client)"""
    return {"message": "client PUT 요청 성공"}

@client_router.delete("/sample-delete")
def client_sample_delete():
    """DELETE 샘플 엔드포인트 (client)"""
    return {"message": "client DELETE 요청 성공"}
