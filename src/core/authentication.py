import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.core.settings import get_settings

_security: HTTPBasic = HTTPBasic()


async def basic_authentication(
    credentials: HTTPBasicCredentials = Depends(_security),
) -> str:
    settings = get_settings()
    current_username = credentials.username.encode("utf8")
    correct_username = settings.fastapi.authentication.username.encode("utf8")
    is_correct_username = secrets.compare_digest(current_username, correct_username)
    current_password = credentials.password.encode("utf8")
    correct_password = settings.fastapi.authentication.password.encode("utf8")
    is_correct_password = secrets.compare_digest(current_password, correct_password)
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
