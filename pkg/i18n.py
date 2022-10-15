from pydantic import BaseModel


class Message(BaseModel):
    singular: str
    plural: str = ""


def new_message(singular: str, plural: str = "") -> Message:
    return Message(singular=singular, plural=plural)
