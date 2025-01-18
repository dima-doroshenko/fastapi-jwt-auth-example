import datetime
from typing import Annotated

from sqlalchemy.orm import mapped_column


created_at = Annotated[
    datetime.datetime,
    mapped_column(default=datetime.datetime.now(datetime.timezone.utc)),
]

intpk = Annotated[int, mapped_column(primary_key=True)]
