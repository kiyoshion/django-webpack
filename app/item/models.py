from django.db import models
from user.models import CustomUser
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings
from django import template
import uuid

register = template.Library()

def upload_directory_path(instance, filename):
  return 'item/{}/{}.{}'.format(instance.id, str(uuid.uuid4()), filename.split('.')[-1])

class Tag(models.Model):
  name = models.CharField(max_length=50)

  def __str__(self):
    return self.name

class Item(models.Model):
  title = models.CharField(max_length=50)
  body = models.TextField()
  author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  image = ProcessedImageField(blank=True,
    null=True,
    upload_to=upload_directory_path,
    processors=[ResizeToFill(1500, 1000)],
    options={'quality': 80})
  image_thumbnail = ImageSpecField(source='image',
    processors=[ResizeToFill(600, 400)],
    options={'quality': 80})
  image_small = ImageSpecField(source='image',
    processors=[ResizeToFill(150, 150)],
    options={'quality': 80})
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  tags = models.ManyToManyField(Tag)

  def __str__(self):
    return '{}({})'.format(self.title, self.author)

  def getSmallImage(self):
    if not self.image:
      return settings.STATIC_URL + 'img/noimage.svg'
    else:
      return self.image_small.url

  def getThumbnailImage(self):
    if not self.image:
      return settings.STATIC_URL + 'img/noimage.svg'
    else:
      return self.image_thumbnail.url

  def save(self, *args, **kwargs):
    if self.id is None:
      uploaded_file = self.image

      self.image = None
      super().save(*args, **kwargs)

      self.image = uploaded_file
      if "force_insert" in kwargs:
        kwargs.pop("force_insert")

    super().save(*args, **kwargs)

class Comment(models.Model):
  body = models.TextField()
  author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
