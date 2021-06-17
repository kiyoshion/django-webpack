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
  paginate_by = 12
  ordering = ['-created_at']

  def get_queryset(self):
    if 'tag' in self.request.GET:
      try:
        tag_id = self.request.GET.get('tag')
        tag = Tag.objects.get(pk=tag_id)
        items = tag.item_set.all()
        return items
      except FieldError:
        return Item.objects.order_by('-created_at')
    elif 'sort' in self.request.GET:
      try:
        sort = self.request.GET.get('sort')
        return Item.objects.annotate(q_count=Count(sort)).order_by('-q_count')
      except FieldError:
        return Item.objects.order_by('-created_at')
    else:
      return Item.objects.order_by('-created_at')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    items = Item.objects.select_related('author').prefetch_related(Prefetch('comment_set', queryset=Comment.objects.all().select_related('author').order_by('-created_at'), to_attr='comments')).prefetch_related(Prefetch('likes', to_attr='islike')).annotate(commentcnt=Count('comment')).all().order_by('-created_at')
    cdict = {}
    ldict = {}
    likecnt = {}
    for i in items:
      likecnt[i.id] = len(i.islike)
      print(i.islike)
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
        if n == 3:
          break
      cdict[i.id] = commenters

    context['commenterslist'] = cdict
    context['islike'] = ldict
    context['likecnt'] = likecnt

    # try:
    #   hero = items.latest("created_at")
    #   if hero.image:
    #     context['hero'] = hero.getThumbnailImage()
    #   else:
    #     context['hero'] = settings.STATIC_URL + 'img/bg-0.jpg'
    # except Item.DoesNotExist:
    #   print('404')
    # for i in items:
    #   print(vars(i))
    context['object_list'] = items
    print(context['commenterslist'])
    return context

class ItemDetail(DetailView):
  model = Item
  template_name = 'item/detail.html'

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
