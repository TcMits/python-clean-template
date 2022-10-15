from datetime import timedelta

from jwt import InvalidTokenError

from pkg.jwt import create_token, jwt_decode


def test_jwt_workflow():
    original_payload = {"test": "nha", "foo": "bar"}
    token = create_token(original_payload, timedelta(days=1), "Dummy")

    payload = jwt_decode(token, "Dummy")

    for k, v in original_payload.items():
        assert payload[k] == v

    assert "iat" in payload
    assert "exp" in payload
