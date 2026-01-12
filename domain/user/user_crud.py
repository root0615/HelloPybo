"""
CryptContext : 비밀번호 암호화를 담당하는 도구 "bcrypt" 같은 안전한 해시 알고리즘을 사용
비밀번호를 원래 값으로 되돌릴 수 없게 만든다.
"""
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import User

"""
비밀번호 암호화 방식정의
schemes=["bcrypt"] : "bcrypt"알고리즘 사용
deprecated="auto" : 최신/안전한 방식만 재사용함
"""
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user_create: UserCreate):
    # 위에 만들어진 CryptContext의 인스턴스 pwd_context로 사용자가 입력한 비밀번호를 hash()로 암호화
    db_user = User(username=user_create.username,
                   password=pwd_context.hash(user_create.password1),
                   email=user_create.email)
    db.add(db_user)
    db.commit()

