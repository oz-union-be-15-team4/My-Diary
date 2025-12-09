import jwt
import os
from datetime import datetime, timedelta, timezone

SECRET_KEY = os.getenv("SECRET_KEY")

def create_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=1),  # 만료 시간
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload   # 정상 -> payload(dict) 반환
    except jwt.ExpiredSignatureError:
        return None      # 만료된 토큰
    except jwt.InvalidTokenError:
        return None      # 잘못된 토큰