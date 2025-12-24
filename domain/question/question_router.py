from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

# from database import SessionLocal
from database import get_db
from domain.question import question_schema, question_crud
# from models import Question

# 라우터 파일에 반드시 필요한 것은 APIRouter 클래스로 생성한 router 객체이다.
# 해당 객체를 FastAPI 앱에 등록해야만 라우팅 기능이 동작한다.
# 그러므로 생성 후 main.py 앱에 등록하자
router = APIRouter(
    # prefix 속성은 요청 URL에 항상 포함되는 값이며,
    # 예시로 밑에 있는 question_list 함수를 불러오려면 "/api/question/list"로 불러야 한다.
    prefix="/api/question",
)

"""
Depends를 사용하면 더 간단하게 사용 가능하다.
FastAPI의 Depends는 매개변수로 전달 받은 함수(get_db)를 호출하여 그 결과를 리턴한다.
따라서 db: Session = Depends(get_db)의 db 객체는 get_db 제너레이터 함수가 yield를 통해 생성한 세션 객체가 주입된다.
FastAPI는 제너레이터 기반함수를 직접 지원하며, 자동으로 리소를 관리를 처리하기에 @contextlib.contextmanager를 사용하면
get_db 함수가 해당 객체(contextlib._GeneratorContextManager)를 반환하기 때문에 FastAPI의 종속성 주입이 제대로 동작 못한다.
따라서 get_db함수에서 @contextlib.contextmanager 어노테이션을 제거해야 사용가능하다.
"""
# response_model=list[question_schema.Question]의 의미는 question_list 함수의 리턴값은 Question 스키마로 구성된 리스트임을 의미
# 만약 Question 스키마에서 content 항목을 삭제하면 해당 API 출력 항목에서도 content 항목은 제거된다. 그러므로 _question_list를 수정할 필요가 없다.
# @router.get("/list", response_model=list[question_schema.Question])
# 페이징 기능을 위해 response_model을 QuestionList로 변경해서 사용한다.
@router.get("/list", response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db), page: int = 0, size: int = 10):
    # db = SessionLocal()
    # _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    # db.close()      # 사용한 세션을 커넥션 풀에 반환(세션 종료가 아님)

    # contextlib.contextmanager를 사용한 버전, 오류 여부 상관없이 with문을 벗어나는 순간 db.close() 자동 실행된다.
    # with get_db() as db:
    #     _question_list = db.query(Question).order_by(Question.create_date.desc()).all()

    # CRUD 파일로 분리하기 위해 주석처리 후 내용 옮김
    # _question_list = db.query(Question).order_by(Question.create_date.desc()).all()   

    # _question_list = question_crud.get_question_list(db)

    # 함수에 page와 size 파라미터를 추가하여 page가 0번 일때 0번 부터 10개의 데이터(index: 0~9)를 가져오게끔 생성하였다.
    total, _question_list = question_crud.get_question_list(db, skip=page*size, limit=size)

    # return _question_list

    # 페이징 출력을 위한 스키마가 변경되었으니 스키마에 맞는 속성으로 리턴값(딕셔너리)을 반환한다.
    return {
        'total': total,
        'question_list': _question_list
    }

# question_id와 같은 가변적인 숫자값을 얻으려면 {} 괄호를 사용하여 경로를 설정해야한다.
@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id=question_id)
    return question

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create: question_schema.QuestionCreate,
                    db: Session = Depends(get_db)):
    question_crud.create_question(db=db, question_create=_question_create)