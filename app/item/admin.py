from django.contrib import admin
from .models import Item, Tag, Comment, Like

admin.site.register(Item)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Like)
