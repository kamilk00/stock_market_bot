import smtplib
from email.mime.text import MIMEText

class SMTPMailManager():
    """
    A class responsible for managing SMTP email sending, including establishing connection, 
    authenticating, and sending emails with specified content and recipients.
    """

    def __init__(self, smtp_server: str, smtp_port: int, email_user: str, email_password: str):
        """
        Initializes the SMTPMailManager with the necessary email credentials and SMTP server details.

        :param smtp_server: The address of the SMTP server (e.g., 'smtp.gmail.com').
        :param smtp_port: The port to use for the SMTP server (typically 587 for TLS).
        :param email_user: The email address used to authenticate the SMTP connection.
        :param email_password: The password or app password for the email account.
        """
        self.SMTP_SERVER = smtp_server
        self.SMTP_PORT = smtp_port
        self.EMAIL_USER = email_user
        self.EMAIL_PASSWORD = email_password


    def send_email(self, subject: str, body: str, recipient_email: str):
        """
        Sends an email with the specified subject, body, and recipient email address.

        :param subject: The subject of the email.
        :param body: The body content of the email.
        :param recipient_email: The recipient's email address.
        """
        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = self.EMAIL_USER
        message["To"] = recipient_email

        try:
            with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as server:
                server.starttls()
                server.login(self.EMAIL_USER, self.EMAIL_PASSWORD)
                server.sendmail(self.EMAIL_USER, recipient_email, message.as_string())
                print('Mail sent successfully')
        except smtplib.SMTPAuthenticationError:
            print("Authentication failed: Check your email or password.")
        except smtplib.SMTPConnectError:
            print("Failed to connect to the SMTP server.")
        except smtplib.SMTPRecipientsRefused:
            print(f"Recipient {recipient_email} refused. Check the email address.")
        except Exception as ex:
            print("Unexpected error during sending email:", ex)