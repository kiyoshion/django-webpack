from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
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
