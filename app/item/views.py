from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

from .models import ItemModel

class ItemList(ListView):
  model = ItemModel
  template_name = 'item/list.html'

class ItemDetail(DetailView):
  model = ItemModel
  template_name = 'item/detail.html'

class ItemCreate(CreateView):
  model = ItemModel
  template_name = 'item/create.html'
  fields = ('title', 'body')
  success_url = reverse_lazy('item.list')

class ItemDelete(DeleteView):
  model = ItemModel
  template_name = 'item/delete.html'
  success_url = reverse_lazy('item.list')

class ItemUpdate(UpdateView):
  model = ItemModel
  template_name = 'item/update.html'
  fields = ('title', 'body')
  success_url = reverse_lazy('item.list')
