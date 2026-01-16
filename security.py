"""
pwdlib + Argon2id로 암호화하는 방법
"""
from pwdlib import PasswordHash

# 현재 기본: Argon2 (argon2id 문자열 형태로 저장됨) :contentReference[oaicite:2]{index=2}
password_hash = PasswordHash.recommended()

# 패스워드를 암호화
def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

# 비밀번호가 서로 맞는지 확인
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)