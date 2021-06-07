from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

from .models import Item

class ItemList(ListView):
  model = Item
  template_name = 'item/list.html'

class ItemDetail(DetailView):
  model = Item
  template_name = 'item/detail.html'

class ItemCreate(LoginRequiredMixin, CreateView):
  model = Item
  template_name = 'item/create.html'
  fields = ('title', 'body', 'image')
  success_url = reverse_lazy('item.list')

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

class ItemDelete(LoginRequiredMixin, DeleteView):
  model = Item
  template_name = 'item/delete.html'
  success_url = reverse_lazy('item.list')

class ItemUpdate(LoginRequiredMixin, UpdateView):
  model = Item
  template_name = 'item/update.html'
  fields = ('title', 'body', 'image')
  success_url = reverse_lazy('item.list')
