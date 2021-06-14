from django import template
register = template.Library()

@register.filter(name="myfilter")
def myfilter(item,user):
  ilike = item.likes.filter(user=user).exists()
  return ilike
