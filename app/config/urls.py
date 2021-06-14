from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from . import views
from user.views import HomeDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    # path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('home/', HomeDetail.as_view(), name='home'),
    path('accounts/', include('allauth.urls')),
    path('user/', include('user.urls')),
    path('item/', include('item.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
