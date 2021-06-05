from django.contrib.auth.models import AbstractUser
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
import uuid

class CustomUser(AbstractUser):
  class Meta:
    db_table = 'custom_user'

  def user_directory_path(instance, filename):
    return 'user/{}/{}.{}'.format(instance.user.id, str(uuid.uuid4()), filename.split('.')[-1])

  avatar = models.ImageField(blank=True, null=True, upload_to=user_directory_path)
  avatar_thumbnail = ImageSpecField(source='avatar',
    processors=[ResizeToFill(150, 150)],
    options={'quality': 80})
