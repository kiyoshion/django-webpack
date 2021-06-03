from django.db import models

class ItemModel(models.Model):
  title = models.CharField(max_length=50)
  body = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
