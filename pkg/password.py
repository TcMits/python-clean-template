import bcrypt


def get_hashed_password(password: str) -> str:
    if not password:
        return ""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(13)).decode("utf-8")


def validate_password(hashed_password: str, password: str) -> bool:
    if not hashed_password or not password:
        return False
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
