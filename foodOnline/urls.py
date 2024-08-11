from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from marketplace import views as marketplaceViews
from accounts import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.home, name='home'),
                  path('', include('accounts.urls')),
                  path('marketplace/', include('marketplace.urls')),
                  # CART
                  path('cart/', marketplaceViews.cart, name='cart'),
                  # SEARCh
                  path('search/',marketplaceViews.search, name='search'),
                  # CHECKOUT
                  path('checkout/',marketplaceViews.checkout, name='checkout'),
                  # ORDERS
                  path('orders/',include('orders.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
