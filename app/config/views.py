from django.views.generic import TemplateView
from item.models import Item

class IndexView(TemplateView):
  template_name = 'index.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['item_list'] = Item.objects.all()
    return context

index = IndexView.as_view()

class HomeView(TemplateView):
  template_name = 'home.html'

home = HomeView.as_view()
