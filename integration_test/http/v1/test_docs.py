import requests
from fastapi import status

from integration_test.http.v1.constants import DOCS_PATH


def test_docs():
    assert requests.get(DOCS_PATH).status_code == status.HTTP_200_OK
