from datetime import timedelta, datetime, UTC

from fastapi import Depends

import jwt
from jwt import InvalidTokenError

from config import settings
from repository import User

from .meta import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, TOKEN_TYPE_FILED, oauth2_scheme
from ..exc import InvalidTokenException, InvalidTokenTypeException, UserNotFoundException


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.now(UTC)

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(to_encode, private_key, algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    deocded = jwt.decode(token, public_key, [algorithm])
    return deocded


def create_jwt(
    token_data: dict,
    token_type: str,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FILED: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: User) -> str:
    jwt_payload = {
        "sub": user.user_id,
    }
    return create_jwt(
        token_data=jwt_payload,
        token_type=ACCESS_TOKEN_TYPE,
        expire_minutes=settings.auth_jwt.access_token_expire_minutes,
    )


def create_refresh_token(user: User) -> str:
    jwt_payload = {
        "sub": user.user_id,
    }
    return create_jwt(
        token_data=jwt_payload,
        token_type=REFRESH_TOKEN_TYPE,
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days),
    )


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
):
    try:
        payload = decode_jwt(token)
    except InvalidTokenError as e:
        raise InvalidTokenException
    return payload


def validate_token_type(payload: dict, token_type: str) -> bool:
    if payload.get(TOKEN_TYPE_FILED) == token_type:
        return True
    raise InvalidTokenTypeException
