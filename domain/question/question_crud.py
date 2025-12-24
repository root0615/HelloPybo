from datetime import datetime

from domain.question.question_schema import QuestionCreate
from models import Question
from sqlalchemy.orm import Session

# 기존에 question_router 파일에 있던 함수 내용을 그대로 가져왔다. (분리하기 위함)
def get_question_list(db: Session, skip: int = 0, limit: int = 10):
    _question_list = db.query(Question)\
        .order_by(Question.create_date.desc())

    # 현재 전체 질문 수를 count한다.
    total = _question_list.count()
    # skip과 limit을 추가했다. skip은 조회한 데이터의 시작위치, limit은 시작위치 부터 가져올 데이터 수를 의미
    question_list = _question_list.offset(skip).limit(limit).all()
    return total, question_list

def get_question(db: Session, question_id: int):
    # question = db.query(Question).get(question_id)        # SQLAlchemy 1.x 버전 스타일
    question = db.get(Question, question_id)                # SQLAlchemy 2.0 버전 스타일
    return question

def create_question(db: Session, question_create:QuestionCreate):
    db_question = Question(subject=question_create.subject,
                           content=question_create.content,
                           create_date=datetime.now())
    db.add(db_question)
    db.commit()