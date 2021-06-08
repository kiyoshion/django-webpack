from django import forms
from .models import Item, Tag
from imagekit.forms import ProcessedImageField

class CreateItemForm(forms.ModelForm):

  class Meta:
    model = Item
    fields = ['title', 'body', 'image', 'tags']

  title = forms.CharField()
  body = forms.CharField(widget=forms.Textarea)
  image = ProcessedImageField(spec_id='app:item:image', required=False)

  tags = forms.CharField(required=False)
