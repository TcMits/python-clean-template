from pkg.password import get_hashed_password, validate_password


def test_password_workflow():
    password = "12345678"

    hashed_password = get_hashed_password(password)
    assert hashed_password != "12345678"
    assert validate_password(hashed_password, password)
