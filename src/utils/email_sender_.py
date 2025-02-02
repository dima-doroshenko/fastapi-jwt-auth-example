import smtplib

from config import settings


class EmailSender:

    def __init__(
        self,
        email: str = settings.email.login,
        password: str = settings.email.password,
        server: str = settings.email.server,
        port: int = settings.email.port
    ):
        self.server = smtplib.SMTP(server, port)
        self.server.starttls()
        self.email = email
        self.server.login(email, password)

    def send_msg(self, to_email: str, text: str, subject: str = settings.app.name) -> None:
        if not settings.email.debug:
            self.server.sendmail(
                from_addr=self.email,
                to_addrs=to_email,
                msg=f'Subject: {subject}\n\n{text}'
            )

email_sender = EmailSender()