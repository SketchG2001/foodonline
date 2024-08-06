from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.home, name='home'),
                  path('', include('accounts.urls')),
                  path('marketplace/', include('marketplace.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
