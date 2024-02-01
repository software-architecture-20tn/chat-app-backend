import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings
from django.dispatch import receiver
from django.template.loader import render_to_string

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender,
    instance,
    reset_password_token,
    *args,
    **kwargs,
) -> None:
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:

    """
    # Set your SMTP server details
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587
    smtp_username = settings.EMAIL_HOST_USER
    # Temporary solutions
    # I will take a look at this later
    # Now I am hurry
    # TODO: Fix this
    smtp_password = settings.EMAIL_HOST_PASSWORD

    # Create message container
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Password Reset for {title}".format(title="The Connect")
    msg['From'] = "theconnectteam@outlook.com"
    msg['To'] = reset_password_token.user.email

    # Set the email content
    context = {
        "current_user": reset_password_token.user,
        "username": reset_password_token.user.username,
        "email": reset_password_token.user.email,
        "reset_password_url": "{}?token={}".format(
            "https://teleclone.nguyenvanloc.name.vn/forgot-password-confirm",
            reset_password_token.key,
        ),
    }

    email_html_message = render_to_string("email/password_reset_email.html", context)
    email_plaintext_message = render_to_string("email/password_reset_email.txt", context)

    # Attach HTML and plain text content
    msg.attach(MIMEText(email_plaintext_message, 'plain'))
    msg.attach(MIMEText(email_html_message, 'html'))
    # breakpoint()

    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
