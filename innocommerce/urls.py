"""innocommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Error Page
    path('404', views.Error404, name='404'),
    path('account/my-account', views.my_account, name='account'),

    path('admin/', admin.site.urls),
    path('base/', views.base, name='base'),
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('product', views.product, name='product'),
    path('product/filter-data',views.filter_data,name="filter-data"),
    path('contact-us', views.contact_us, name='contact_us'),
    path('product/<slug:slug>', views.PRODUCT_DETAILS, name='product_detail'),
    path('account/register', views.user_register, name='user_register'),
    path('account/login', views.user_login, name='user_login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('account/profile', views.profile, name="profile"),
    path('account/profile/update', views.profile_update, name="profile_update"),

    # Carts
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),

    


    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
