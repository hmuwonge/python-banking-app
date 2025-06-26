from cloudinary import logger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_otp_email(email,otp):
    subject = _('Your OTP code for Login')
    from_email = settings.DEFAULT_FROM_EMAIL
    receipient_list = [email]
    context={
        "otp":otp,
        "expiry_time": settings.OTP_EXPIRATION,
        "site_name": settings.SITE_NAME,
    }
    html_email = render_to_string('emails/otp_email.html',context)
    plain_email = strip_tags(html_email)
    email =EmailMultiAlternatives(subject,plain_email,from_email,receipient_list)
    email.attach_alternative(html_email,'text/html')
    try:
        email.send()
        logger.info(f"OTP email sent successfully to: {email}")

    except Exception as e:
        logger.error(f"Failed to send OTP to {email}: Error: {str(e)}")


def send_accountLocked_email(self):
    subject = _('Your Account Has Been Locked')
    from_email = settings.DEFAULT_FROM_EMAIL
    receipient_list = [self.email]
    context={
        "user":self,
        "expiry_time": int(settings.LOCKOUT_DURATION.total_seconds()//60),
        "site_name": settings.SITE_NAME,
    }
    html_email = render_to_string('emails/account_locked.html',context)
    plain_email = strip_tags(html_email)
    email =EmailMultiAlternatives(subject,plain_email,from_email,receipient_list)
    email.attach_alternative(html_email,'text/html')
    try:
        email.send()
        logger.info(f"Account locked email sent to: {self.email}")

    except Exception as e:
        logger.error(f"Failed to send account locked email to {self.email}: Error: {str(e)}")