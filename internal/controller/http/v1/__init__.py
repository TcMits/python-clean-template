from fastapi import FastAPI


def get_handler() -> FastAPI:
    return FastAPI()
