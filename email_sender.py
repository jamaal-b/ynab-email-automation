"""
Email sender module
Handles SMTP email sending with HTML templates
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import Optional


class EmailSender:
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        username: str,
        password: str,
        from_email: str
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_email = from_email
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ):
        """Send an HTML email"""
        msg = MIMEMultipart("alternative")
        
        # Properly encode subject with UTF-8
        msg["Subject"] = Header(subject, 'utf-8')
        msg["From"] = self.from_email
        msg["To"] = to_email
        
        # Add plain text version if provided
        if text_content:
            text_part = MIMEText(text_content, "plain", "utf-8")
            msg.attach(text_part)
        
        # Add HTML version with UTF-8 encoding
        html_part = MIMEText(html_content, "html", "utf-8")
        msg.attach(html_part)
        
        # Send email
	# Send email
        try:
            print(f"  Connecting to {self.smtp_server}:{self.smtp_port}...")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                print(f"  Starting TLS...")
                server.starttls()
                print(f"  Logging in as {repr(self.username)}...")
                server.login(self.username, self.password)
                print(f"  Sending message...")
                server.send_message(msg)
                print(f"✓ Email sent: {subject}")
        except Exception as e:
            print(f"✗ Failed to send email: {subject}")
            print(f"  Error: {str(e)}")
            print(f"  Username: {repr(self.username)}")
            print(f"  From: {repr(self.from_email)}")
            print(f"  To: {repr(to_email)}")
            import traceback
            traceback.print_exc()
            raise
