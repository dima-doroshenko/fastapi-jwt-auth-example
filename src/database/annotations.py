import datetime
from typing import Annotated

from sqlalchemy.orm import mapped_column

now = lambda: datetime.datetime.now(datetime.timezone.utc)

created_at = Annotated[
    datetime.datetime,
    mapped_column(default=now)
]

intpk = Annotated[int, mapped_column(primary_key=True)]
