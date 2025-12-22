# create_engine: 데이터베이스와 실제로 연결을 만들어주는 Engine을 생성하는 함수이다. SQL을 실행하고 커넥션 풀을 관리하는 핵심 객체
from sqlalchemy import create_engine
# declarative_base : ORM 모델(테이블과 매핑되는 클래스)을 만들 때 공통 부모 클래스를 생성해주는 함수이며
# 메타 데이터(테이블 정의)를 한데 모을 수 있다
from sqlalchemy.ext.declarative import declarative_base
# sessionmaker: DB와 대화 창구인 Session 객체를 만들어주는 공장 함수를 가져옴
# 쿼리 실행, 추가, 삭제 등 작업 전부 Session에서 이루어짐
from sqlalchemy.orm import sessionmaker

# 사용할 데이터 베이스 주소
SQLALCHEMY_DATABASE_URL = "sqlite:///./myapi.db"

# 위 URL로 Engine(DB 연결 관리자)를 만듭니다.
# check_same_thread = False의 의미는 SQLite는 기본적으로 같은 스레드에서만 연결을 사용하도록 제한하여
# FastAPI(uvicorn)는 요청을 여러 스레드에서 처리할 수 있으니 이제한을 풀어 여러 스레드에 같은 연결을 쓸수 있게 한다.
# 이건 SQLite 전용 옵션으로 Postgresql 등을 쓰면 보통 connect_args 없이 생성.
# create_engine은 커넥션 풀을 생성한다. 커넥션 풀이란 데이터베이스에 접속하는 객체를 일정 갯수 만큼 만들어 놓고 돌려가며 사용하는 것을 말한다.
# 다시 정리하면 데이터베이스에 접속하는 세션 수를 제어하고 세션접속에 소요되는 시간을 줄이고자하는 용도로 사용한다. 
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# bind=engine: engine에 연결되는 Session 클래스를 만들어줌, 이후 db = SessionLocal() 처럼 실제 세션 인스턴스를 뽑아 씀.
# autocommit=False: 명시적으로 db.commit() 할 때만 트랜잭션이 확정, 실수로 자동 커밋 막아줌
# autoflush=False : 쿼리를 날리기 직전에 자동으로 변경분을 DB에 반영하지 않게 합니다.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM 베이스 클래스 만듦
Base = declarative_base()