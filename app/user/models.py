from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
import uuid

class CustomUser(AbstractUser):
  class Meta:
    db_table = 'custom_user'

  def user_directory_path(instance, filename):
    return 'user/{}/{}.{}'.format(instance.id, str(uuid.uuid4()), filename.split('.')[-1])

  displayname = models.CharField(max_length=50, default='', blank=True, null=True)
  profile = models.TextField(default='', blank=True, null=True)
  avatar = ProcessedImageField(blank=True,
    null=True,
    upload_to=user_directory_path,
    processors=[ResizeToFill(150, 150)],
    options={'quality': 80})

  def getAvatar(self):
    if not self.avatar:
      return settings.STATIC_URL + 'img/avatar.svg'
    else:
      return self.avatar.url
