from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class ItemModel(models.Model):
  title = models.CharField(max_length=50)
  body = models.TextField()
  image = models.ImageField(blank=True, null=True, upload_to='item/')
  image_thumbnail = ImageSpecField(source='image',
    processors=[ResizeToFill(600, 400)],
    options={'quality': 80})
  image_big = ImageSpecField(source='image',
    processors=[ResizeToFill(1500, 1000)],
    options={'quality': 80})
  image_small = ImageSpecField(source='image',
    processors=[ResizeToFill(150, 150)],
    options={'quality': 80})


  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
