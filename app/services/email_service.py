import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from app.core.config import settings


class EmailService:
    def __init__(self):
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_username = settings.smtp_username
        self.smtp_password = settings.smtp_password
        self.smtp_from_email = settings.smtp_from_email
        self.smtp_from_name = settings.smtp_from_name

        template_dir = Path(__file__).parent.parent / "templates"
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))

    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        body_html: str | None = None,
    ) -> bool:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{self.smtp_from_name} <{self.smtp_from_email}>"
        message["To"] = to_email

        message.attach(MIMEText(body, "plain"))

        if body_html:
            message.attach(MIMEText(body_html, "html"))

        try:
            async with aiosmtplib.SMTP(
                hostname=self.smtp_host, port=self.smtp_port
            ) as smtp:
                await smtp.login(self.smtp_username, self.smtp_password)
                await smtp.send_message(message)
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    async def send_welcome_email(self, to_email: str, name: str) -> bool:
        subject = "Welcome to FastAPI Boilerplate"
        body = f"Hello {name},\n\nWelcome to FastAPI Boilerplate!"
        body_html = f"<h1>Welcome {name}!</h1><p>Welcome to FastAPI Boilerplate!</p>"
        return await self.send_email(to_email, subject, body, body_html)

    async def send_password_reset_email(self, to_email: str, reset_token: str) -> bool:
        subject = "Password Reset Request"
        reset_link = f"http://localhost:3000/reset-password?token={reset_token}"
        body = f"Click this link to reset your password: {reset_link}"
        body_html = f"""
        <html>
        <body>
            <h2>Password Reset Request</h2>
            <p>You requested to reset your password. Click the link below to proceed:</p>
            <a href="{reset_link}">Reset Password</a>
            <p>This link will expire in 1 hour.</p>
            <p>If you didn't request this, please ignore this email.</p>
        </body>
        </html>
        """
        return await self.send_email(to_email, subject, body, body_html)


email_service = EmailService()

