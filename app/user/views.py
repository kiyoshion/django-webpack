from django.db.models import query
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse

from .models import CustomUser

class UserDetail(DetailView):
  model = CustomUser
  template_name = 'user/detail.html'

class UserUpdate(LoginRequiredMixin, UpdateView):
  model = CustomUser
  template_name = 'user/update.html'
  fields = ('displayname', 'avatar', 'profile')
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
    # new_avatar = CustomUser.objects.filter(pk=pk).update(avatar=avatar)
    return JsonResponse({ 'url': user.avatar.url})
