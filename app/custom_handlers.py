import os
import logging

from django.utils.log import AdminEmailHandler
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from . import settings


class MyCustomAdminEmailHandler(AdminEmailHandler):

    def emit(self, record):
        if record.levelno == logging.ERROR:
            html_message = self.format(record)

            subject = 'New Issue'
            email = os.getenv('ADMIN')

            html_content = render_to_string(
                f'html_messages/mail_admin.html',
                {
                    'trace': html_message,
                }
            )

            message = EmailMultiAlternatives(
                subject=subject,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email]
            )
            print(email)
            message.attach_alternative(html_content, 'text/html')
            message.send()

