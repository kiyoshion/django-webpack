from django.db.models import query
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpRequest

from .models import CustomUser
from item.models import Item, Comment

class HomeDetail(TemplateView):
  model = CustomUser
  template_name = 'home.html'

  def get_context_data(self):
    context = super().get_context_data()
    items = Item.objects.filter(author=self.request.user).order_by('-created_at')
    try:
      hero = items.latest("created_at")
      context['hero'] = hero.getThumbnailImage()
    except Item.DoesNotExist:
      print('404')
    likes = Item.objects.filter(likes__user=self.request.user).order_by('-likes__created_at')
    comments = Comment.objects.filter(author=self.request.user).order_by('-created_at')
    context['items'] = items
    context['likes'] = likes
    context['comments'] = comments

    return context

class UserDetail(DetailView):
  model = CustomUser
  context_object_name = "items"
  template_name = 'user/detail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    items = Item.objects.filter(author=self.object.id)
    likes = Item.objects.filter(likes__author=self.object.id)
    context['items'] = items
    context['likes'] = likes

    return context

class UserUpdate(LoginRequiredMixin, UpdateView):
  model = CustomUser
  template_name = 'user/update.html'
  fields = ('displayname', 'profile')
  success_url = reverse_lazy('home')

  def get_queryset(self):
    queryset = super().get_queryset()

    return queryset.filter(id=self.request.user.id)

def AvatarUpload(request, pk):
  if request.method == 'POST':
    avatar = request.FILES['avatar']
    user = CustomUser.objects.get(pk=pk)
    user.avatar = avatar
    user.save(update_fields=['avatar'])
    
    return JsonResponse({ 'url': user.avatar.url})
