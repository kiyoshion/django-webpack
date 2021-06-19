from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views
from item.views import IndexView, HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('home/', HomeView.as_view(), name='home'),
    path('accounts/', include('allauth.urls')),
    path('user/', include('user.urls')),
    path('item/', include('item.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
  import debug_toolbar

  urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
