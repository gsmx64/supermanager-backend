import smtplib
from django.conf import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MailService:
    def __init__(self) -> None:
        self.smtp_server = settings.MAIL_HOST
        self.smtp_port = settings.MAIL_PORT
        self.smtp_username = settings.MAIL_USER
        self.smtp_password = settings.MAIL_PASSWORD
        self.use_tls = settings.MAIL_USE_TLS
        self.use_ssl = settings.MAIL_USE_SSL
        self.from_email = settings.DEFAULT_FROM_EMAIL

    def send_email(self, *, to_email, subject, body) -> bool:
        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                elif self.use_ssl:
                    server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
