# server.py
import uvicorn
from fastapi import FastAPI, Request

# FastAPI 앱 생성
app = FastAPI()


@app.post("/echo")
async def echo(request: Request):
    payload = await request.json()
    return payload


if __name__ == "__main__":
    print("🚀 FastAPI echo 서버를 http://localhost:8080 에서 시작합니다.")
    print("클라이언트 실행 전, 이 서버를 먼저 실행해 주세요.")
    uvicorn.run(app, host="0.0.0.0", port=8080)
