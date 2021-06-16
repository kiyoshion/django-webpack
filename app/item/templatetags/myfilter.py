from django import template
register = template.Library()

@register.filter(name="myfilter")
def myfilter(item,user):
  ilike = item.likes.filter(user=user).exists()
  return ilike

@register.filter(name="get_item")
def get_item(dictionary, key):
  return dictionary.get(key)
