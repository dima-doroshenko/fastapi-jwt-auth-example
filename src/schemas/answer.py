from pydantic import BaseModel


class Answer(BaseModel):
    ok: bool = True
    data: dict | None = None
    detail: str | None = None
