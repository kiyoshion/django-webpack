from django.conf import settings
from django.db.models import Count, Prefetch
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpRequest

from .models import CustomUser
from item.models import Item, Comment
from item.views import ItemList

class HomeDetail(TemplateView):
  model = CustomUser
  template_name = 'home.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    context['myitems'] = Item.objects.filter(author=self.request.user).order_by('-created_at')

    return context



'''
OK HERE=====
  model = Item
  template_name = 'home.html'
  queryset = Item.objects.select_related('author').prefetch_related(Prefetch('comment_set', queryset=Comment.objects.all().select_related('author').order_by('-created_at'), to_attr='comments')).prefetch_related(Prefetch('likes', to_attr='islike')).annotate(commentcnt=Count('comment')).all()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    items = self.queryset.filter(author=self.request.user).order_by('-created_at')
    context['myitems'] = items

    try:
      hero = items.latest('created_at')
      context['hero'] = hero.getThumbnailImage()
    except Item.DoesNotExist:
      context['hero'] = settings.STATIC_URL + 'img/noimage.png'

    mylikes = self.queryset.filter(likes__user=self.request.user).order_by('-likes__created_at')
    context['mylikes'] = mylikes

    mycomments = []
    for c in self.queryset.comment_set.select_related('author').filter(comment_set__author=self.request.user).order_by('-created_at'):
      comment = {
        'username': c.author.username,
        'avatar': c.author.getAvatar(),
        'created_at': c.created_at,
        'body': c.body
      }
      mycomments.append(comment)
    context['mycomments'] = mycomments

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
'''






  # def get_context_data(self):
  #   context = super().get_context_data()
  #   items = Item.objects.filter(author=self.request.user).order_by('-created_at')
  #   try:
  #     hero = items.latest("created_at")
  #     context['hero'] = hero.getThumbnailImage()
  #   except Item.DoesNotExist:
  #     print('404')
  #   likes = Item.objects.filter(likes__user=self.request.user).order_by('-likes__created_at')
  #   comments = Comment.objects.filter(author=self.request.user).order_by('-created_at')
  #   context['items'] = items
  #   context['likes'] = likes
  #   context['comments'] = comments

  #   return context





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
