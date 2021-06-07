from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy

from .models import CustomUser

class UserDetail(DetailView):
  model = CustomUser
  template_name = 'user/detail.html'

class UserUpdate(LoginRequiredMixin, UpdateView):
  model = CustomUser
  template_name = 'user/update.html'
  fields = ('displayname', 'avatar', 'profile')
  success_url = reverse_lazy('home')
