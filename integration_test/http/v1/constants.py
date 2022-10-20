# REST
HOST = "http://python"
PORT = "8000"
HEAL_PATH = HOST + "/ping"

V1_SUBPATH = "/api/v1"
LOGIN_SUBPATH = V1_SUBPATH + "/login"
REFRESH_TOKEN_SUBPATH = V1_SUBPATH + "/refresh-token"
VERIFY_TOKEN_SUBPATH = V1_SUBPATH + "/verify-token"
DOCS_SUBPATH = V1_SUBPATH + "/docs"

LOGIN_PATH = HOST + LOGIN_SUBPATH
REFRESH_TOKEN_PATH = HOST + REFRESH_TOKEN_SUBPATH
VERIFY_TOKEN_PATH = HOST + VERIFY_TOKEN_SUBPATH
DOCS_PATH = HOST + DOCS_SUBPATH
