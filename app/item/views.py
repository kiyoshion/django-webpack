from .forms import CreateItemForm
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.http.response import JsonResponse
from django.conf import settings
from django.db.models import Count, Prefetch
from django.core.exceptions import FieldError
from .models import Item, Tag, Comment, Like
from user.models import CustomUser

class ItemList(ListView):
  allow_empty = True
  model = Item
  template_name = 'item/list.html'
  ordering = '-created_at'
  paginate_by = 6
  queryset = Item.objects.select_related('author').prefetch_related(Prefetch('comment_set', queryset=Comment.objects.all().select_related('author').order_by('-created_at'), to_attr='comments')).prefetch_related(Prefetch('likes', to_attr='islike')).annotate(commentcnt=Count('comment')).all()

  def get_queryset(self):
    if 'sort' in self.request.GET and self.request.GET.get('sort') != 'created_at':
      sort = self.request.GET.get('sort')
      try:
        return self.queryset.annotate(sort=Count(sort)).order_by('-sort')
      except FieldError:
        return self.queryset.order_by('-created_at')
    else:
      return self.queryset.order_by('-created_at')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    items = self.get_queryset()
    cdict = {}
    ldict = {}
    likecnt = {}
    for i in items:
      likecnt[i.id] = len(i.islike)
      if not i.islike:
        ldict[i.id] = False
      else:
        for li in i.islike:
          if li.user_id == self.request.user.id:
            ldict[i.id] = True
          else:
            ldict[i.id] = False

      commenters = []
      for n, c in enumerate(i.comments):
        commenters.append(c.author.getAvatar())
        if n == 2:
          break
      cdict[i.id] = commenters

    context['commenterslist'] = cdict
    context['islike'] = ldict
    context['likecnt'] = likecnt
    return context

class ItemDetail(DetailView):
  model = Item
  template_name = 'item/detail.html'
  queryset = Item.objects.select_related('author').prefetch_related(Prefetch('comment_set', queryset=Comment.objects.all().select_related('author').order_by('-created_at'), to_attr='comments')).prefetch_related(Prefetch('tags', to_attr='item_tags')).prefetch_related(Prefetch('likes', to_attr='islike')).annotate(commentcnt=Count('comment')).all()

  def get_queryset(self):
    return self.queryset.filter(id=self.kwargs['pk'])

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    commentlist = []
    for c in self.object.comment_set.select_related('author').all().order_by('-created_at'):
      comment = {
        'username': c.author.username,
        'avatar': c.author.getAvatar(),
        'created_at': c.created_at,
        'body': c.body
      }
      commentlist.append(comment)
    context['commentlist'] = commentlist
    taglist = []
    for t in self.object.item_tags:
      tag = {
        'id': t.id,
        'name': t.name
      }
      taglist.append(tag)
    context['taglist'] = taglist
    return context

class ItemCreate(LoginRequiredMixin, CreateView):
  model = Item
  form_class = CreateItemForm
  template_name = 'item/create.html'

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

    return redirect('item.detail', pk=item.id)

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

    return redirect('item.detail', pk=item.id)

def create_comment(request, pk):

  if request.method == 'POST':
    item = Item.objects.get(pk=pk)
    comment = Comment(body=request.POST.get('comment'), author=request.user, item=item)
    comment.save()
    return redirect('item.detail', pk=pk)

def delete_item(request, pk):

  if request.method == 'POST':
    item = Item.objects.get(pk=pk)
    if item.author == request.user:
      item.delete()
      data = {"msg": 'ok'}
    else:
      data = {"msg": 'ng'}

  return JsonResponse(data)

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
  else:
    data = {"msg": 'Bad method'}

  return JsonResponse(data)
