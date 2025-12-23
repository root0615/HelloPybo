from models import Question
from sqlalchemy.orm import Session

# 기존에 question_router 파일에 있던 함수 내용을 그대로 가져왔다. (분리하기 위함)
def get_question_list(db: Session):
    question_list = db.query(Question)\
        .order_by(Question.create_date.desc())\
        .all()
    return question_list

