from django.views.generic import TemplateView
from django.conf import settings
from item.models import Item

class IndexView(TemplateView):
  template_name = 'index.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['item_list'] = Item.objects.all().order_by('-created_at')[:3]
    try:
      hero = Item.objects.latest("created_at")
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
