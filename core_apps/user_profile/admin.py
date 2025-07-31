from django.contrib import admin
from cloudinary.forms import CloudinaryFileField
from django import forms
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import NextOfKin,UserProfile
# Register your models here.

class ProfileAdminFrom(forms.ModelForm):
    photo = CloudinaryFileField(
        options= {"crop": "thumb", "width":200,"height":200,"folder":"bank_photos"},
        required=False,
    )

    class Meta:
        model = UserProfile
        fields = '__all__'

class NextOfKinInline(admin.TabularInline):
    model = NextOfKin
    extra = 1
    fields=["first_name","last_name","relationship","phone_number","is_primary"]

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminFrom
    list_display = ['user','full_name','employment_status','email','phone_number','photo_preview']
    list_display_links = ["user"]
    list_filter = ["gender","marital_status","employment_status","country"]
    search_fields = ["user__email","user__first_name","phone_number"]
    readonly_fields = ["user"]
    fieldsets = (
        _("Personal Information"),
        {
            "fields":(
                "user",
                "photo",
                "is_photo",
                "signature_photo",
                "title",
                "gender",
                "date_of_birth",
                "marital_status",
            )
        },
        (
            _("Contact Information"),
            {
                "fields":
                    ("phone_number","address","city","country")
            },
        ),
        (
            _("Identification"),
            {
            "fields":
            (
            "means_of_identification",
                "id_issue_date",
                "id_expiry_date",
                "passport_number"
        )
            },
        ),
        (
            _("Employment Information"),
            {
                "fields":(
                    "employment_status",
                    "employer_name",
                    "annual_income",
                    "date_of_employment",
                    "employer_city",
                    "employer_state"
                )
            }
        )
    )
    inlines =[NextOfKinInline]

    def full_name(self, obj)->str:
        return obj.user.first_name

    full_name.short_description =_('Full name')

    def email(self, obj)->str:
        return obj.user.email

    email.short_description =_('Email')

    def photo_preview(self, obj)->str:
      if obj.photo:
          return format_html(
              '<img src="{}" width="50" height="50" style="object-fit:cover; />',
              obj.photo.url
          )
      return "No Photo Yet"

    photo_preview.short_description =_("Photo")

@admin.register(NextOfKin)
class NextOfKinAdmin(admin.ModelAdmin):
    list_display = ['full_name','last_name','relationship','profile','is_primary']
    list_filter = ["is_primary"]

