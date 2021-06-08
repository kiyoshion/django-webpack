from django.contrib import admin
from django.urls import path
from . import views
from .views import UserDetail, UserUpdate

urlpatterns = [
    path('<int:pk>/', UserDetail.as_view(), name='user.detail'),
    path('update/<int:pk>/', UserUpdate.as_view(), name='user.update'),
    path('avatarupload/<int:pk>/', views.AvatarUpload),
]
