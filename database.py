# import contextlib

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

"""
# @contextlib.contextmanager
해당 어노테이션은 with문에서 사용할 수 있는 컨텍스트 매니저 객체를 클래스를 만들지 않고 함수로 정의하게 해주는 데코레이터
try/finally로 세션을 가져왔다가 반환하는 반복되는 상황을 편리하게 만들 수 있으며, with문 하나로 안전하게 묶어주는 역할이다.

with get_db() as db:
    # 여기서 db 세션 객체를 사용

하지만 FastAPI의 Depends를 사용할 경우 종속성 주입이 제대로 이루어지지 않아 해당 어노테이션을 제거해야한다.
"""
# @contextlib.contextmanager
def get_db():
    db = SessionLocal()
    try:
        # 제너레이터 방식을 사용해서 세션을 반환한다.
        yield db
    finally:
        db.close()

"""
# 제너레이터란 무엇인가?
제너레이터를 알기 전에 이터레이터를 알아야한다.
이터레이터(iterator)란 next() 함수 호출 시 계속 그 다음 값을 반환하는 객체
예를 들어 리스트와 같은 객체를 반복 가능 객체라 하는데(리스트가 이터레이터라는건 아님) 
이터레이터 객체는 next() 함수로 모두 호출한 후 재 호출 시 다시 읽을 수 없다는 특징이 있다.

제너레이터는 이터레이터를 생성해주는 함수이다. 이터레이터와 마찬가지로 netx() 함수로 값을 차례대로 얻을 수 있는데
차례대로 결과를 반환하고자 return이 아닌 yield 키워드를 사용한다.

def example():
    yield 'a'
    yield 'b'
    yield 'c'

g = example()

next(g) => 'a'
next(g) => 'b'
next(g) => 'c'
"""