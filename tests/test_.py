import pytest

from typing import Any, Callable, Iterable
from httpx import AsyncClient

from repository import User
from utils.auth import decode_jwt

from crud import get_verification_code, get_me


async def test_invalid_login_or_password(ac: AsyncClient):
    response = await ac.post(
        "auth/login",
        data={"username": "admin", "password": "adminadmin"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid login or password"


async def test_unauthed(ac: AsyncClient):
    response = await ac.get("me/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


async def test_registration(ac: AsyncClient):
    response = await ac.post(
        "auth/register",
        json={
            "email": "email@email.com",
            "password": "adminadmin",
            "username": "admin",
        },
    )
    token = response.json()["access_token"]
    ac.headers.update({"Authorization": f"Bearer {token}"})


async def test_login_by_email(ac: AsyncClient):
    response = await ac.post(
        "auth/login",
        data={"username": "email@email.com", "password": "adminadmin"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert decode_jwt(token)["sub"] == 1


async def test_get_me(ac: AsyncClient, test: bool = True) -> dict[str]:
    response = await ac.get("me/")
    assert response.status_code == 200
    json = response.json()
    if not test:
        return json
    assert json["email"] == "email@email.com"
    assert json["username"] == "admin"
    assert json["verified"] == False
    assert json["id"] == 1


async def test_edit_username(ac: AsyncClient):
    response = await ac.patch("/me/", json={"username": "Admin"})
    assert response.status_code == 200
    assert (await test_get_me(ac, test=False))["username"] == "Admin"


@pytest.mark.parametrize("url", ["auth/change-email", "auth/forgot-password"])
async def test_not_verified_user(url: str, ac: AsyncClient):
    response = await ac.post(url)
    assert response.status_code == 403
    assert "email is not verified" in response.json()["detail"]


async def test_verify_email(ac: AsyncClient):
    response = await ac.post("auth/verify")
    assert response.status_code == 200


async def test_confirm_verify_email(ac: AsyncClient):
    code = await get_verification_code()
    response = await ac.post(f"auth/verify/{code}")
    assert response.status_code == 200
    assert (await test_get_me(ac, test=False))["verified"] == True


async def test_token_type_validation(ac: AsyncClient):
    response = await ac.post("auth/refresh")
    assert response.status_code == 401
    assert "Invalid token type" in response.json()["detail"]

@pytest.mark.parametrize(
    "url, data, tests",
    [
        [
            "auth/forgot-password",
            {"password": "newpassword"},
            lambda me: me.check_password("newpassword"),
        ],
        [
            "auth/change-email",
            {'email': "test@example.com"},
            (
                lambda me: me.email == "test@example.com",
                lambda me: me.verified == False,
            )
        ],
    ],
)
async def test_need_verification(
    url: str,
    data: dict,
    tests: Iterable[Callable[[User], Any]] | Callable[[User], Any],
    ac: AsyncClient,
):
    if callable(tests):
        tests = (tests,)

    await ac.post(url)
    response = await ac.post(url + '/', json=dict(code=await get_verification_code(), **data))
    assert response.status_code == 200
    me = await get_me()
    
    for test in tests:
        assert test(me)