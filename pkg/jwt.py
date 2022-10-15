from datetime import datetime, timedelta
from typing import Any, Dict

import jwt

JWT_ALGORITHM = "HS256"


def jwt_base_payload(exp_delta: timedelta) -> Dict[str, Any]:
    utc_now = datetime.utcnow()
    payload = {"iat": utc_now, "exp": utc_now + exp_delta}
    return payload


def jwt_encode(payload: Dict[str, Any], secret: str) -> str:
    tk = jwt.encode(
        payload,
        secret,
        JWT_ALGORITHM,
    )
    return tk.decode("utf-8") if not isinstance(tk, str) else tk


def jwt_decode(token: str, secret: str) -> Dict[str, Any]:
    return jwt.decode(
        token,
        secret,
        algorithms=JWT_ALGORITHM,
    )


def create_token(payload: Dict[str, Any], exp_delta: timedelta, secret: str) -> str:
    p = {**payload, **jwt_base_payload(exp_delta)}
    return jwt_encode(p, secret)
