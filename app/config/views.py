from django.views.generic import TemplateView
from django.db.models import Count
from django.conf import settings
from item.models import Item
from user.models import CustomUser

class IndexView(TemplateView):
  template_name = 'index.html'
  fields = ['id', 'image', 'created_at', 'author_id']

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    items = Item.objects.order_by('-created_at').all()[:3]
    cdict = {}
    ldict = {}
    for i in items:
      com = i.comments.order_by('author').distinct('author').values('id')[:4]
      coms = CustomUser.objects.filter(id__in=com)
      cdict[i.id] = coms
      if self.request.user.is_authenticated:
        islike = i.likes.filter(user=self.request.user).exists()
        ldict[i.id] = islike
    context['islike'] = ldict
    context['commenters'] = cdict
    context['item_list'] = items
    try:
      hero = items.first()
      if hero.image:
        context['hero'] = hero.getThumbnailImage()
      else:
        context['hero'] = settings.STATIC_URL + 'img/bg-0.jpg'
    except Item.DoesNotExist:
      print('404')

    return context

index = IndexView.as_view()

class HomeView(TemplateView):
  template_name = 'home.html'

home = HomeView.as_view()
