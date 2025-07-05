from django.db import models
import uuid
from typing import Any, Optional
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey    
from django.utils.translation import gettext_lazy as _
from django.db import IntegrityError, models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


User = get_user_model() 

class TimeStampedModel(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ContentView(TimeStampedModel):
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        related_name="content_views",
        verbose_name=_("User"),
        null=True,
        blank=True
    )
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name=_("Content Type")
    )
    object_id = models.UUIDField(verbose_name=_("Object ID"))
    content_object = GenericForeignKey("content_type", "object_id")
    viewer_ip = models.GenericIPAddressField(
        verbose_name=_("Viewer IP Address"),
        null=True,
        blank=True,
    )
    last_viewed_at = models.DateTimeField()
        

    class Meta:
        unique_together = ("user","viewer_ip", "content_type", "object_id")
        verbose_name = _("Content View")
        verbose_name_plural = _("Content Views")

    def __str__(self):
        return (f"{self.content_type} viewed by"
        f"{self.user.get_full_name if self.user else 'Anonymous'} from IP {self.viewer_ip} at {self.last_viewed_at}"
                )
        
    @classmethod
    def record_view(
        cls,content_object: Any, user: Optional[User], viewer_ip: Optional[str])-> None:

        content_type = ContentType.objects.get_for_model(content_object)

        try:
            view, created = cls.objects.get_or_create(
            content_type=content_type,
            object_id=content_object.id,
            defaults={
                "user": user,
                "viewer_ip": viewer_ip,
                "last_viewed_at": timezone.now(),
            },
            )
            if not created:
                view.last_viewed = timezone.now()
        except IntegrityError:
            pass
