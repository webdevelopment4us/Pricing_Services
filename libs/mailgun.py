from requests import Response, post
from typing import List
import os

class MailgunException(Exception):
    def __init__(self, message: str):
        self.message = message

class Mailgun:
    FROM_TITLE =  "Pricing service"
    
    @classmethod
    def send_mail(cls, email: List[str], subject: str, text: str, html: str) -> Response:
        api_key = os.environ.get("MAILGUN_API_KEY", None)
        domain = os.environ.get("MAILGUN_DOMAIN", None)
        EMAIL = os.environ.get("FROM_EMAIL",None)

        if api_key is None:
            raise MailgunException("Failed to load Mailgun API Key.")

        if domain is None:
            raise MailgunException("Failed to load Mailgun domain.")
        response = post(f"{domain}/messages",
                            auth=("api", api_key),
                            data={"from": f"{cls.FROM_TITLE} <{EMAIL}>",
                                "to": email,
                                "subject": subject,
                                "text": text,
                                "html": html})
        if response.status_code != 200:
            print (response.json())
            raise MailgunException('An error occurred while sending e-mail.')
        return response



