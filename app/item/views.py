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

class ItemList(ListView):
  allow_empty = True
  model = Item
  template_name = 'item/list.html'
  ordering = '-created_at'
  paginate_by = 6
  values = ('id', 'title', 'body', 'created_at', 'author_id', 'author_id__username', 'author_id__avatar', 'image', 'likes__user_id', 'likes__user_id__avatar')
  values_comment = ('id', 'body', 'created_at', 'item_id', 'author_id', 'author_id__username', 'author_id__avatar')
  values_like = ('id', 'created_at', 'user_id', 'user_id__avatar', 'user_id__username')
  queryset = (
    Item.objects.all()
      .select_related('author')
      .prefetch_related(
        Prefetch(
          'comment_set',
          queryset=Comment.objects.all().select_related('author').order_by('-created_at').only(*values_comment),
          to_attr='comments'
          )
        )
      .prefetch_related(
        Prefetch(
          'likes',
          queryset=Like.objects.all().select_related('user').order_by('-created_at').only(*values_like),
          to_attr='islike'
          )
      )
      .annotate(
        Count('comment'),
        Count('likes'),
      )
      .only(*values)
  )

  def get_queryset(self):
    if 'sort' in self.request.GET and self.request.GET.get('sort') != 'created_at':
      sort = self.request.GET.get('sort')
      try:
        return self.queryset.annotate(sort=Count(sort)).order_by('-sort', '-created_at')
      except FieldError:
        return self.queryset.order_by('-created_at')
    else:
      return self.queryset.order_by('-created_at')

  def get_item(self, i, list):
    item = {}
    data_item = self.get_item_meta(i)
    item.update(data_item)
    data_likes = self.get_like_meta(i, self.request.user)
    item.update(data_likes)
    data_comments = self.get_comment_meta(i)
    item.update(data_comments)
    list.append(item)
    return list

  def get_item_meta(self, item):
    data = {
      'id': item.id,
      'title': item.title,
      'body': item.body,
      'image': item.getThumbnailImage(),
      'author': {
        'id': item.author.id,
        'username': item.author.username,
        'avatar': item.author.getAvatar(),
      },
      'created_at': item.created_at
    }
    return data

  def get_like_meta(self, item, user):
    is_like = False
    for l in item.islike:
      if l.user_id == user.id:
        is_like = True
        break
      else:
        is_like = False
    data = {
      'likes': {
        'cnt': item.likes__count,
        'islike': is_like
      }
    }
    return data

  def get_comment_meta(self, item):
    list = []
    limit = 2
    for n, c in enumerate(item.comments):
      list.append(c.author.getAvatar())
      if n == limit:
        break
    data = {
      'comments': {
        'cnt': item.comment__count,
        'avatars': list,
      }
    }
    return data

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    items = self.get_queryset()
    itemlist = []
    for i in items:
      self.get_item(i, itemlist)
    context['item_list'] = itemlist

    return context

class ItemDetail(DetailView):
  model = Item
  template_name = 'item/detail.html'
  values = ('id', 'title', 'body', 'created_at', 'author_id', 'author_id__username', 'author_id__avatar', 'image', 'likes__user_id', 'likes__user_id__avatar')
  values_comment = ('id', 'body', 'created_at', 'item_id', 'author_id', 'author_id__username', 'author_id__avatar')
  values_like = ('id', 'created_at', 'user_id', 'user_id__avatar', 'user_id__username')
  queryset = (
    Item.objects.all()
      .select_related('author')
      .prefetch_related(
        Prefetch(
          'comment_set',
          queryset=Comment.objects.all().select_related('author').order_by('-created_at').only(*values_comment),
          to_attr='comments'
          )
        )
      .prefetch_related(
        Prefetch(
          'likes',
          queryset=Like.objects.all().select_related('user').order_by('-created_at').only(*values_like),
          to_attr='islike'
          )
      )
      .prefetch_related(Prefetch('tags', to_attr='item_tags'))
      .annotate(
        Count('comment'),
        Count('likes'),
      )
      .only(*values)
  )

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


class IndexView(ItemList):
  template_name = 'index.html'

  def get_queryset(self):
    return super().get_queryset()[:3]

index = IndexView.as_view()

class HomeView(ItemList):
  template_name = 'home.html'

  def get_comment(self, c, list):
    comment = {
      'username': c.author.username,
      'avatar': c.author.getAvatar(),
      'created_at': c.created_at,
      'body': c.body,
      'item_id': c.item_id
    }
    list.append(comment)
    return list

  def get_context_data(self, **kwargs):
    context = {}
    items = self.get_queryset()

    # For myitems
    myitems = items.filter(author=self.request.user)
    myitemlist = []
    for i in myitems:
      self.get_item(i, myitemlist)
    context['myitems'] = myitemlist

    try:
      hero = myitems.first()
      context['hero'] = hero.getThumbnailImage()
    except (Item.DoesNotExist, AttributeError):
      context['hero'] = settings.STATIC_URL + 'img/bg-0.jpg'

    # For mylikes
    mylikes = items.filter(likes__user=self.request.user).order_by('-likes__created_at')
    mylikelist = []
    for i in mylikes:
      self.get_item(i, mylikelist)
    context['mylikes'] = mylikelist

    # For mycomments
    mycomments = []
    precomments = Comment.objects.filter(author=self.request.user).select_related('author').order_by('-created_at')
    if precomments.exists():
      for c in precomments:
        self.get_comment(c, mycomments)
      context['mycomments'] = mycomments
    else:
      context['mycomments'] = False

    print(context)
    return context
