from django.contrib import admin
from django.urls import path
from . import views
from .views import ItemList, ItemDetail, ItemCreate, ItemDelete, ItemUpdate, ItemTagList

urlpatterns = [
    path('', ItemList.as_view(), name='item.list'),
    path('<int:pk>/', ItemDetail.as_view(), name='item.detail'),
    path('create/', ItemCreate.as_view(), name='item.create'),
    path('delete/<int:pk>/', ItemDelete.as_view(), name='item.delete'),
    path('del/<int:pk>/', views.delete_item, name='delete_item'),
    path('update/<int:pk>/', ItemUpdate.as_view(), name='item.update'),
    path('create_comment/<int:pk>/', views.create_comment, name='item.create_comment'),
    path('like/<int:pk>/', views.like, name='item.like'),
    path('tag/<int:pk>/', ItemTagList.as_view(), name='item.tag_list'),
]
