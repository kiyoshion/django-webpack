from django.contrib import admin
from django.urls import path
from .views import ItemList, ItemDetail, ItemCreate

urlpatterns = [
    path('', ItemList.as_view(), name='item.list'),
    path('<int:pk>/', ItemDetail.as_view(), name='item.detail'),
    path('create/', ItemCreate.as_view(), name='item.create'),
]
