from pydantic import BaseModel, field_validator

class AnswerCreate(BaseModel):
    content: str

    # content 필드에 대해 검증 로직을 적용하겠다는 선언, content에 값이 들어올때마다 자동실행(여러개 필드 지정가능)
    # get 방식이 아닌 다른 방식(post, put, delete)의 입력값은 Pydantic 스키마로만 읽을 수 있기에 해당 방법을 사용
    @field_validator('content')     
    def not_empty(cls, v):          # cls: 클래스 자체(AnswerCreate), v: 실제로 전달된 content값
        # not v: 빈 문자열 또는 None일 경우 True, not v.strip(): 공백만 있을 경우 True
        # 결국 값이 없거나 공백만 있는 경우 에러 발생하게 함
        if not v or not v.strip():  
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v        # 검증에 통과하면 반환
