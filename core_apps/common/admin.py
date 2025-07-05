from django.contrib import admin

# Register your models here.

from typing import Any
from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import ContentView

@admin.register(ContentView)
class ContentViewAdmin(GenericTabularInline):
    list_display =[
        "user",
        "content_object",
        "content_type",
        "viewer_ip",
        "last_viewed",
        "last_viewed_at",
        "created_at",
        "updated_at"
        ]
    list_filter = ["content_type", "last_viewed", "created_at"]
    search_fields = ["user__email", "content_type__model", "viewer_ip"]
    readonly_fields = [
        "content_type",
        "object_id", 
        "content_object",
        "user",
        "last_viewed_at",
        "viewer_ip",
        "created_at",
        "updated_at"]
    fieldsets = (
        (           
           None,
            {
                "fields": (
                    "content_type",
                    "object_id",
                    "content_object",
                )
            },
        ),
        (_("View Details"),
            {
                "fields": (
                    "user",
                    "viewer_ip",
                    "last_viewed_at",
                )
            }),
        (
            _("Timestamps"),
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )
    
    def has_add_permission(self, request: HttpRequest)-> bool:
        return False
        
    def has_change_permission(
        self, request: HttpRequest, obj: Any = None
    )-> bool:
        return False
    
class ContentViewInline(GenericTabularInline):
    model = ContentView
    extra = -1
    readonly_fields = [
        "user", "content_type",
        "viewer_ip", "last_viewed_at",
        "created_at", "updated_at"]
    can_delete = False
    show_change_link = True
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False