import uuid

from celery.utils.time import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .emails import send_accountLocked_email
from .managers import UserManager
# Create your models here.

class User(AbstractUser):
    class SecurityQuestions(models.TextChoices):
        MAIDEN_NAME = "maiden_name", _("What is your mother's maiden name?")
        FAVOURITE_COLOR = "favourite_color", _("What is your favourite color?")
        BIRTH_CITY = "birth_city", _("What is the city where you were born?")
        CHILDHOOD_FRIEND = "childhood_friend", _("What is the name of your childhood best friend?")

    class AccountStatus(models.TextChoices):
        ACTIVE = "active", _("Account is active")
        LOCKED = "locked", _("Account is locked")

    class RoleChoices(models.TextChoices):
        CUSTOMER = "customer", _("Customer")
        ACCOUNT_EXECUTIVE = "account_executive", _("Account executive")
        TELLER = "teller", _("Teller")
        BRANCH_MANAGER = "branch_manager", _("Branch manager")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(_("Username"),max_length=50, unique=True)
    security_question = models.CharField(
        _("Security Question"), max_length=50,
        choices=SecurityQuestions.choices,
    )
    security_answer = models.CharField(_("Security Answer"), max_length=255)
    email = models.EmailField(_("Email"), unique=True,db_index=True)
    first_name = models.CharField(_("First Name"),max_length=50)
    middle_name = models.CharField(_("Middle Name"),max_length=50,blank=True, null=True)
    last_name = models.CharField(_("Last Name"),max_length=50)
    id_no =models.PositiveIntegerField(_("ID Number"),unique=True)
    account_status = models.CharField(_("Account Status"), max_length=20,
                                      choices=AccountStatus.choices,
                                      default=AccountStatus.ACTIVE)
    role = models.CharField(_("Role"),max_length=20,
                            choices=RoleChoices.choices,
                            default=RoleChoices.CUSTOMER)
    failed_login_attempts = models.PositiveSmallIntegerField(default=0)
    last_failed_login_attempts = models.DateTimeField(_("Last Failed Login Attempts"),blank=True, null=True)
    otp =models.CharField(_("OTP"),max_length=6,blank=True)
    otp_expiry_time = models.DateTimeField(_("OTP Expiry Time"),blank=True, null=True)

    objects = UserManager()
    USERNAME_FIELD="email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "id_no",
        "security_question",
        "security_answer",
    ]

    def set_otp(self, otp:str)->None:
        self.otp =otp
        self.otp_expiry_time = timezone.now() + settings.OTP_EXPIRATION
        self.save()

    def verify_otp(self, otp:str)->None:
        if self.otp == otp and self.otp_expiry_time > timezone.now():
            self.otp=""
            self.otp_expiry_time =None
            self.save()
            return True
        return False

    def handle_failed_login_attempts(self)->None:
        self.failed_login_attempts += 1
        self.last_failed_login_attempts = timezone.now()
        if self.failed_login_attempts >= settings.LOGIN_ATTEMPTS:
            self.account_status = self.AccountStatus.LOCKED
            self.save()
            send_accountLocked_email(self)
        self.save()

    def reset_failed_login_attempts(self)->None:
        self.failed_login_attempts = 0
        self.account_status = self.AccountStatus.ACTIVE
        self.save()

    def unlock_account(self)->None:
        if self.account_status == self.AccountStatus.LOCKED:
            self.account_status = self.AccountStatus.ACTIVE
            self.failed_login_attempts = 0
            self.last_failed_login_attempts = None
            self.save()

    @property
    def is_locked_out(self)->bool:
        if self.account_status == self.AccountStatus.LOCKED:
            if( self.last_failed_login_attempts and (timezone.now() - self.last_failed_login_attempts)
                    > settings.LOCKOUT_DURATION):
                self.unlock_account()
                return False
            return True
        return False

    @property
    def full_name(self)->str:
        full_name =f"{self.first_name} {self.last_name}"
        return full_name.title().strip()

    class Meta:
        verbose_name =_("User")
        verbose_name_plural = _("Users")
        ordering = ["-date_joined"]

    def has_role(self, role_name:str)->bool:
        return hasattr(self, "role") and self.role == role_name

    def __str__(self)->str:
        return f"{self.first_name} - {self.get_role_display()}"

