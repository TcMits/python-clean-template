import requests
from fastapi import status

from integration_test.http.v1.constants import REFRESH_TOKEN_PATH, VERIFY_TOKEN_PATH
from integration_test.http.v1.helpers import (
    get_authenticated_payload,
    get_token,
    session_context,
)
from pkg.models.factories.user import UserFactory


def test_login():
    with session_context():
        UserFactory.create(username="foofoofoo", password="barbarbar")
        authenticated_payload = get_authenticated_payload("foofoofoo", "barbarbar")
        assert bool(authenticated_payload.get("access_token"))
        assert bool(authenticated_payload.get("refresh_token"))
        assert bool(authenticated_payload.get("refresh_key"))


def test_verify_token():
    with session_context():
        UserFactory.create(username="foofoofoo", password="barbarbar")
        token = get_token("foofoofoo", "barbarbar")
        assert (
            requests.post(VERIFY_TOKEN_PATH, data={"token": token}).status_code
            == status.HTTP_200_OK
        )


def test_refresh_token():
    with session_context():
        UserFactory.create(username="foofoofoo", password="barbarbar")
        authenticated_payload = get_authenticated_payload("foofoofoo", "barbarbar")

        assert bool(
            requests.post(
                REFRESH_TOKEN_PATH,
                data={
                    "refresh_token": authenticated_payload["refresh_token"],
                    "refresh_key": authenticated_payload["refresh_key"],
                },
            )
            .json()
            .get("token")
        )
