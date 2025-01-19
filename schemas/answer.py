from pydantic import BaseModel, Field


class Answer(BaseModel):
    ok: bool = True
    data: dict | None = None
    detail: str | None = None
