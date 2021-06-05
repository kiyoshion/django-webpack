from django.contrib.auth.models import AbstractUser
from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
import uuid


class CustomUser(AbstractUser):
  class Meta:
    db_table = 'custom_user'

  def user_directory_path(instance, filename):
    return 'user/{}/{}.{}'.format(instance.id, str(uuid.uuid4()), filename.split('.')[-1])

  avatar = ProcessedImageField(blank=True,
    null=True,
    upload_to=user_directory_path,
    processors=[ResizeToFill(150, 150)],
    options={'quality': 80})
