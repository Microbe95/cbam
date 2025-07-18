from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/chatbot/generate/")
async def generate_chatbot_response(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    # 실제 챗봇 로직은 여기에 구현 (예시: echo)
    result = f"챗봇 응답: {prompt}"
    return JSONResponse(content={"result": result}) 