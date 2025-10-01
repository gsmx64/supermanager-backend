import pytest

from unittest.mock import patch, MagicMock
from api.services.mail import MailService


@pytest.fixture
def mail_service():
    with patch("api.services.mail.settings") as mock_settings:
        mock_settings.MAIL_HOST = "smtp.example.com"
        mock_settings.MAIL_PORT = 587
        mock_settings.MAIL_USER = "user@example.com"
        mock_settings.MAIL_PASSWORD = "password"
        mock_settings.MAIL_USE_TLS = True
        mock_settings.MAIL_USE_SSL = False
        mock_settings.DEFAULT_FROM_EMAIL = "noreply@example.com"
        yield MailService()

def test_send_email_success_tls(mail_service):
    with patch("smtplib.SMTP") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        result = mail_service.send_email(
            to_email="recipient@example.com",
            subject="Test Subject",
            body="Test Body"
        )
        assert result is True
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("user@example.com", "password")
        mock_server.send_message.assert_called_once()

def test_send_email_success_ssl(mail_service):
    mail_service.use_tls = False
    mail_service.use_ssl = True
    with patch("smtplib.SMTP_SSL") as mock_smtp_ssl:
        mock_server = MagicMock()
        mock_smtp_ssl.return_value = mock_server
        with patch("smtplib.SMTP") as mock_smtp:
            result = mail_service.send_email(
                to_email="recipient@example.com",
                subject="Test Subject",
                body="Test Body"
            )
        assert result is True
        mock_smtp_ssl.assert_called_once_with("smtp.example.com", 587)
        mock_server.login.assert_called_once_with("user@example.com", "password")
        mock_server.send_message.assert_called_once()

def test_send_email_failure(mail_service):
    with patch("smtplib.SMTP") as mock_smtp:
        mock_server = MagicMock()
        mock_server.login.side_effect = Exception("Login failed")
        mock_smtp.return_value.__enter__.return_value = mock_server
        result = mail_service.send_email(
            to_email="recipient@example.com",
            subject="Test Subject",
            body="Test Body"
        )
        assert result is False

def test_send_email_sets_headers(mail_service):
    with patch("smtplib.SMTP") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        mail_service.send_email(
            to_email="recipient@example.com",
            subject="Header Test",
            body="Body"
        )
        sent_msg = mock_server.send_message.call_args[0][0]
        assert sent_msg['From'] == "noreply@example.com"
        assert sent_msg['To'] == "recipient@example.com"
        assert sent_msg['Subject'] == "Header Test"
