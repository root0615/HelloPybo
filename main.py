from fastapi import FastAPI
# CORSMiddleware : Starlette(=FastAPI의 기반 프레임워크)에서 제공하는 미들웨어로, CORS 정책을 처리하는 역할 담당
from starlette.middleware.cors import CORSMiddleware

from domain.answer import answer_router
from domain.question import question_router

# FastAPI 서버 인스턴스 생성.
app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # 허용할 출처(도메인) 목록. 리스트로 전달
    allow_credentials=True,     # True일 경우, 쿠키나 인증정보를 포함한 요청도 허용
    allow_methods=["*"],        # 어떤 HTTP 메서드를 허용할지 지정. "*"의 경우 모두 허용, 다른 경우 ["GET", "POST"]
    allow_headers=["*"],        # 허용할 요청헤더. 마찬가지로 모두 허용
)

# 필요 없어져서 제외함.
# @app.get("/hello")
# def hello():
#     return {"message": "안녕하세요 파이보"}

# ========= router 객체 등록 =========
app.include_router(question_router.router)
app.include_router(answer_router.router)