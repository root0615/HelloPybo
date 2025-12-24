from datetime import datetime

from domain.question.question_schema import QuestionCreate
from models import Question
from sqlalchemy.orm import Session

# 기존에 question_router 파일에 있던 함수 내용을 그대로 가져왔다. (분리하기 위함)
def get_question_list(db: Session):
    question_list = db.query(Question)\
        .order_by(Question.create_date.desc())\
        .all()
    return question_list

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