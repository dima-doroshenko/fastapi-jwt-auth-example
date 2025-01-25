from config import settings

class EmailSender:

    def __init__(
        email: str = settings.email.login,
        password: str = settings.email.password
    ):
        ...

    def send_msg(self, to_email: str, text: str) -> None:
        print(f'Message to: {to_email}\nText: {text}')

email_sender = EmailSender()