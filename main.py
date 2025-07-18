from fastapi import APIRouter

# account_router 생성
account_router = APIRouter()

@account_router.get("/sample-get")
def account_sample_get():
    """GET 샘플 엔드포인트 (account)"""
    return {"message": "account GET 요청 성공"}

@account_router.post("/sample-post")
def account_sample_post():
    """POST 샘플 엔드포인트 (account)"""
    return {"message": "account POST 요청 성공"}

@account_router.put("/sample-put")
def account_sample_put():
    """PUT 샘플 엔드포인트 (account)"""
    return {"message": "account PUT 요청 성공"}

@account_router.delete("/sample-delete")
def account_sample_delete():
    """DELETE 샘플 엔드포인트 (account)"""
    return {"message": "account DELETE 요청 성공"}