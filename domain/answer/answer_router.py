from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.answer import answer_schema, answer_crud
from domain.question import question_crud

router = APIRouter(
    prefix="/api/answer",
)

"""
답변 등록을 처리할 answer_create 라우터 함수를 생성
- 입력: answer_schema.AnswerCreate
- 출력: 없음
API 호출시 파라미터로 전달한 content가 AnswerCreate 스키마에 자동으로 매핑되고
출력은 response_model을 사용하는 대신 204 응답 코드를 리턴하여 응답없음을 나타낸다.

작성한 라우터는 main.py로 등록
"""
@router.post("/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_create(question_id: int,
                  _answer_create: answer_schema.AnswerCreate,
                  db: Session = Depends(get_db)):
    # create answer
    question = question_crud.get_question(db, question_id=question_id)
    if not question:
        # 질문 객체가 존재하지 않을 경우 HTTPException 오류가 발생하게 했다.
        raise HTTPException(status_code=404, detail="Question not found")

    answer_crud.create_answer(db, question=question, answer_create=_answer_create)

