from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# 앞서 database.py에서 정의한 Base 클래스를 상속하기 위해 가져옴
from database import Base

class Question(Base):
    __tablename__ = "question"  # 모델에 의해 관리되는 테이블 이름
    
    # 고유번호, 제목, 내용, 작성일시 속성으로 구성
    # Column 함수의 첫번째 인수는 데이터 타입이며 그 외에 다른 속성을 추가로 설정 가능하다.
    id = Column(Integer, primary_key=True)          # primary_key로 기본키를 설정한다.
    subject = Column(String, nullable=False)        # nullable은 Null 값을 허용할지의 여부를 판단한다.
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)

class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    # 답변은 어떤 질문에 대한 답변인지 알아야 함으로 Question클래스의 id 속성이 필요하여 외부키를 지정
    question_id = Column(Integer, ForeignKey("question.id"))
    # relationship으로 question 속성을 생성하면, 답변 객체에서 연결된 질문의 제목을 answer.question.subject 처럼 참조 가능
    # 한 질문에는 여러개의 답변이 달릴 수 있는데 역참조(backref)는 이 질문에 달린 답변들을 참조할 수 있게 된다. EX) a_question.answers
    question = relationship("Question", backref="answers")