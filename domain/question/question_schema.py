import datetime

"""
Pydantic은 FastAPI의 입출력 스펙을 정의하고 그 값을 검증하기 위해 사용하는 라이브러리이다.

- 입출력 항목의 갯수와 타입을 설정
- 입출력 항목의 필수값 체크
- 입출력 항목의 데이터 검증

Pydantic을 사용하기 위한 스키마를 생성하였다.
이와 같이 스키마로 정의한 내용은 router 함수에 적용한다.
"""
from pydantic import BaseModel

from domain.answer.answer_schema import Answer

# Question 스키마 (question_router안에 있는 router함수에 적용)
class Question(BaseModel):
    # 총 4개의 출력 항목을 정의하고 데이터 타입을 지정
    # 만약 필수 항목이 아니라고 설정하려면? ex) subject: str | None = None
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: list[Answer] = []