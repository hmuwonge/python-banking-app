from typing import Any

from django.db import models
from cloudinary.models import CloudinaryField
from django.conf import settings
from django.contrib.auth import  get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from core_apps.common.models import  TimeStampedModel
# Create your models here.

User = get_user_model()

class UserProfile(TimeStampedModel):
    class Salutation(models.TextChoices):
        MR = ("mr",_("Mr"),)
        MRS = ("mrs",_("Mrs"),)
        MISS = ("miss",_("Miss"),)

    class Gender(models.TextChoices):
        MALE = ("male",_("Male"),)
        FEMALE = ("female",_("Female"),)

    class MaritalStatus(models.TextChoices):
        MARRIED = ("married",_("Married"),)
        DIVORCED = ("divorced",_("Divorced"),)
        SINGLE = ("single",_("Single"),)
        WIDOWED = ("widowed",_("Widowed"),)
        SEPARATED = ("separated",_("Separated"),)
        UNKNOWN = ("unknown",_("Unknown"),)

    class IdentificationMeans(models.TextChoices):
        DRIVERS_LICENSE = ("drivers_license",_("Drivers License"),)
        NATIONAL_ID = ("national_id",_("National ID"),)
        PASSPORT = ("passport",_("Passport"),)

    class EmploymentStatus(models.TextChoices):
        SELF_EMPLOYED = ("self_employed",_("Self Employed"),)
        EMPLOYED = ("employed",_("Employed"),)
        UN_EMPLOYED = ("unemployed",_("Unemployed"),)
        RETIRED = ("retired",_("Retired"),)
        STUDENT = ("student",_("Student"),)

    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="profile")
    title = models.CharField(_("Salutation"), max_length=10, choices=Salutation.choices,default=Salutation.MR.value)
    gender = models.CharField(_("Gender"), max_length=10, choices=Gender.choices,default=Gender.MALE.value)
    date_of_birth = models.DateField(_("Date of Birth"), blank=True, default=settings.DEFAULT_DATE_OF_BIRTH)
    country_of_birth = CountryField(_("Country of Birth"), blank=True, default=settings.DEFAULT_COUNTRY)
    place_of_birth =models.CharField(_("Place of Birth"), max_length=100, blank=True, default="Unknown")
    marital_status = models.CharField(_("Marital Status"),max_length=10,
                                     choices=MaritalStatus.choices,default=MaritalStatus.UNKNOWN.value)
    means_of_identification = models.CharField(_("Identification Means"),max_length=100,
                                           choices=IdentificationMeans.choices,default=IdentificationMeans.DRIVERS_LICENSE.value())
    id_issue_date = models.DateField(_("ID or Passport Issue Date"),default=settings.DEFAULT_DATE)
    id_expiry_date = models.DateField(_("ID or Passport Expiry Date"),default=settings.DEFAULT_EXPIRY_DATE)
    passport_number  =models.CharField(_("Passport Number"), max_length=20, blank=True, null=True)
    nationality = models.CharField(_("Nationality"), max_length=30, blank=True, null=True,default="unknown")
    phone_number = PhoneNumberField(_("Phone Number"), max_length=30, blank=True, null=True,default="unknown")
    address = models.CharField(_("Address"), max_length=30, blank=True, null=True,default="unknown")
    city = models.CharField(_("City"), max_length=30, blank=True, null=True,default="unknown")
    country = CountryField(_("Country"), blank=True, default=settings.DEFAULT_COUNTRY)
    employment_status = models.CharField(_("Employment Status"),max_length=100,
                                        choices=EmploymentStatus.choices,default=EmploymentStatus.SELF_EMPLOYED.value)
    employer_name = models.CharField(_("Employer Name"), max_length=50, blank=True, null=True)
    annual_income = models.CharField(_("Annual Income"), max_length=12, decimal_place=1,default=0.0)
    date_of_employement = models.DateField(_("Date of Employment"), blank=True, null=True)
    employer_address = models.CharField(_("Employer Address"), max_length=100, blank=True, null=True)
    employer_city = models.CharField(_("Employer City"), max_length=100, blank=True, null=True)
    employer_state = models.CharField(_("Employer State"), max_length=100, blank=True, null=True)
    photo = CloudinaryField(_("Photo"), null=True, blank=True, default=None)
    photo_url =models.URLField(_("Photo URL"), null=True, blank=True, default=None)

    id_photo = CloudinaryField(_("ID Photo"), null=True, blank=True, default=None)
    id_photo_url =models.URLField(_("ID Photo URL"), null=True, blank=True, default=None)
    signature_photo =CloudinaryField(_("Signature Photo"), null=True, blank=True, default=None)
    signature_photo_url= models.URLField(_("Signature Photo URL"), null=True, blank=True, default=None)

    def clean(self)->None:
        super().clean()
        if self.id_issue_date and self.id_expiry_date:
            if self.id_expiry_date <= self.id_issue_date:
                raise ValidationError(_("ID Expiry Date must be greater than issue date"))
            
    def save(
        self,
        *args,
        **kwargs
    )->None:
        self.full_clean()
        super().save(*args, **kwargs)

    def is_complete_with_next_of_kin(self):
        required_fields=[
            self.title,
            self.gender,
            self.date_of_birth,
            self.country_of_birth,
            self.place_of_birth,
            self.marital_status,
            self.means_of_identification,
            self.id_issue_date,
            self.id_expiry_date,
            self.nationality,
            self.phone_number,
            self.address,
            self.city,
            self.country,
            self.employment_status,
            self.photo,
            self.id_photo,
            self.signature_photo,
        ]

        return all(required_fields) and self.next_of_kin.exists

    def __str__(self)->str:
        return f"{self.title} {self.user.firs_name}'s Profile"

class NextOfKin(TimeStampedModel):
    class Salutation(models.TextChoices):
        MR = ("mr", _("Mr"),)
        MRS = ("mrs", _("Mrs"),)
        MISS = ("miss", _("Miss"),)

    class Gender(models.TextChoices):
        MALE = ("male", _("Male"),)
        FEMALE = ("female", _("Female"),)

    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="next_of_kin")
    title = models.CharField(_("Salutation"), max_length=5, choices=Salutation.MR.value)
    first_name = models.CharField(_("First Name"), max_length=50, blank=True, null=True)
    last_name = models.CharField(_("Last Name"), max_length=50, blank=True, null=True)
    other_names = models.CharField(_("Other Names"), max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(_("Date of Birth"), blank=True, default=settings.DEFAULT_DATE)
    gender = models.CharField(_("Gender"),max_length=8,choices=Gender.MALE.value)
    relationship = models.CharField(_("Relationship"), max_length=50, blank=True, null=True)
    email_address = models.EmailField(_("Email Address"), blank=True, null=True)
    phone_number = PhoneNumberField(_("Phone Number"), max_length=50, blank=True, null=True)
    address = models.CharField(_("Address"), max_length=100, blank=True, null=True)
    city = models.CharField(_("City"), max_length=100, blank=True, null=True)
    country = models.CharField(_("Country"), max_length=100, blank=True, null=True)
    is_primary = models.BooleanField(_("Is Primary Next of Kin"), default=False)

    def clean(self)->None:
        super().clean()
        if self.is_primary:
            primary_kin = NextOfKin.objects.filter(
                profile = self.profile,is_primary=True
            ).exclude(pk=self.pk)
            if primary_kin.exists():
                raise ValidationError(_("There can only be one primary next of kin"))

    def save(self,*args: Any,**kwargs: Any) -> None:
        self.full_clean()
        super().save(*args,**kwargs)

    def __str__(self)->str:
        return f"{self.first_name} {self.last_name} - Next of Kin for {self.profile.user.full_name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "is_primary"],
                condition=models.Q(is_primary=True),
                name="unique_primary_next_of_kin",
            )
        ]