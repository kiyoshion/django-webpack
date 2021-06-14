from .forms import CreateItemForm
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, FormView
from django.urls import reverse_lazy
from django.http import Http404
from django.http.response import JsonResponse

from .models import Item, Tag, Comment, Like

class ItemList(ListView):
  allow_empty = True
  model = Item
  template_name = 'item/list.html'

  def get_queryset(self):
    return Item.objects.order_by('-created_at')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    try:
      hero = Item.objects.latest("created_at")
      context['hero'] = hero.getThumbnailImage()
    except Item.DoesNotExist:
      print('404')
    return context


# class ItemTagList(ListView):
#   model = Item
#   template_name = 'item/tag_list.html'

class ItemDetail(DetailView):
  model = Item
  template_name = 'item/detail.html'

  # def get_context_data(self, **kwargs):
  #   context = super().get_context_data(**kwargs)
  #   try:
  #     item = Item.object.get(pk=self.pk)
  #     comments = item.comments_set.all()
  #     context['comments_cnt'] = comments.count()
  #     context['comments_usrs'] =

class ItemCreate(LoginRequiredMixin, CreateView):
  model = Item
  form_class = CreateItemForm
  template_name = 'item/create.html'
  success_url = reverse_lazy('item.list')

  def form_valid(self, form):
    success_url = 'item.list'
    item = form.save(commit=False)
    item.author = self.request.user
    item.save()
    tags = self.request.POST['tags'].split(',')

    if tags:
      for tag_name in tags:
        tag_name = tag_name.strip()
        if tag_name != '':
          exist = Tag.objects.filter(name=tag_name).first()
          if exist:
            item.tags.add(exist)
          else:
            item.tags.create(name=tag_name)
    return redirect(success_url)

class ItemDelete(LoginRequiredMixin, DeleteView):
  model = Item
  template_name = 'item/delete.html'
  success_url = reverse_lazy('item.list')

  def get_queryset(self):
    queryset = super().get_queryset()
    return queryset.filter(author=self.request.user)

class ItemUpdate(LoginRequiredMixin, UpdateView):
  model = Item
  form_class = CreateItemForm
  template_name = 'item/update.html'
  success_url = reverse_lazy('item.list')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    tags = self.object.tags.all()
    arr = []
    for tag in tags:
      arr.append(tag.name)
    context['tag_arr'] = arr
    return context

  def get_queryset(self):
    queryset = super().get_queryset()
    return queryset.filter(author=self.request.user)

  def form_valid(self, form):
    success_url = 'item.list'
    item = form.save(commit=False)
    item.save()

    # Remove current tags
    current_tags = item.tags.all()
    for current_tag in current_tags:
      item.tags.remove(current_tag)
      if current_tag.item_set.count() == 0:
        current_tag.delete()

    # Add or Create request tags
    tags = self.request.POST['tags'].split(',')
    if tags:
      for tag_name in tags:
        tag_name = tag_name.strip()
        if tag_name != '':
          exist = Tag.objects.filter(name=tag_name).first()
          if exist:
            item.tags.add(exist)
          else:
            item.tags.create(name=tag_name)
    # return redirect(success_url)
    return redirect('item.detail', pk=item.id)

def create_comment(request, pk):

  if request.method == 'POST':
    item = Item.objects.get(pk=pk)
    comment = Comment(body=request.POST.get('comment'), author=request.user, item=item)
    comment.save()
    return redirect('item.detail', pk=pk)

def like(request, pk):

  if request.method == 'POST':
    item = Item.objects.get(pk=pk)
    like = item.likes.filter(user=request.user)
    flg = like.exists()
    if flg:
      like.delete()
    else:
      l = Like(user=request.user, item=item)
      l.save()
      item.likes.add(l)
    cnt = item.likes.count()
    data = {"cnt": cnt}
    return JsonResponse(data)
