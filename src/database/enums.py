from enum import Enum


class EmailConfirmationType(Enum):
    verify = 1
    forgot_password = 2
    change_email = 3