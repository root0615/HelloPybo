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
    """
    Answer 테이블에 데이터를 입력할 때 예시
    >> q = db.get(Question, 2)          # question 테이블의 id가 2번인 데이터 행 가져오기
    >> a = Answer(question=q, content='내용 예시', create_date=datetime.now())
    위의 a 객체를 만들 시 Answer 클래스의 question 속성에 위에서 불러온 q 객체를 대입
    이렇게 해줄 경우 question_id의 속성 값은 따로 지정 안해도 자동으로 입력된다.
    그러므로 따로 question_id에 값을 설정할 필요가 없다.
    """

    """
    # sqlalchemy 와 alembic 에 대하여
    - ORM은 sqlalchemy, 스키마 관리 도구가 alembic
    
    # alembic 사용 흐름
    - 최초 사용 시 1회만 적용
    1. SQLAlChemy 모델 작성
    2. 명령어 입력 >> alembic init migrations
    3. alembic 설정 (env.py = sqlalchemy 만든 모델 파일 지정 경로, alembic.ini = 데이터베이스 경로 설정)
    
    - 모델 수정 및 추가 후 반복
    1. SQLAlchemy 모델 수정 및 추가 
    2. 명령어 입력 >> alembic revision --autogenerate -m "메시지"
    3. migration 파일 검토 및 수정
    4. 명령어 입력(해당 명령어 입력시 바로 적용) >> alembic upgrade head
    """