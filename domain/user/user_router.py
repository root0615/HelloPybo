from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session
from starlette import status
from security import verify_password

from database import get_db
from domain.user import user_crud, user_schema

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
# >> openssl rand -hex 32 : 해당 명령어로 아래의 시크릿 키를 생성
SECRET_KEY = "f4572d29c8cf946b511913fa73231b23b611ed3e741ac5948df8bbb3df1b4799"
ALGORITHM = "HS256"

router = APIRouter(
    prefix="/api/user",
)

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    user_crud.create_user(db, user_create=_user_create)

"""
로그인 API 입력항목인 username과 password 값은 OAuth2PasswordRequestForm을 통해 얻어올 수 있다.
"""
@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):

    # check user and password
    # username을 사용해서 사용자 모델 객체(user)를 조회하여 가져온다.
    user = user_crud.get_user(db, form_data.username)
    # 해당 유저가 존재하는지 현재 입력된 password와 데이터베이스에 있는 password와 일치하는지 판단
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            # 해당 사용자를 찾지 못하거나 비밀번호가 일치하지 않다면 HTTP 401오류를 리턴한다.
            # 401 오류는 사용자 인증 오류를 의미한다.
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    data = {
        # 사용자 명
        "sub": user.username,
        # 유효기간
        # datetime.utcnow()는 낡은 방식이므로 사용을 피하라고 경고가 확인되어 변경하여 사용
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    """
    # 필요한 정보 3가지
    ACCESS_TOKEN_EXPIRE_MINUTES : 토큰의 유효기간을 의미. 분 단위로 설정
    SECRET_KEY : 암호화시 사용하는 64자리의 랜덤한 문자열
    ALGORITHM : 토큰 생성시 사용하는 알고리즘을 의미. 여기서는 HS256 사용
    """
    # jwt(JSON Web Token)를 사용하여 엑세스 토큰을 생성한다.
    # jwt는 JSON 포맷을 이용하여 사용자에 대한 속성을 저장하는 Claim 기반의 Web Token이다.
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }