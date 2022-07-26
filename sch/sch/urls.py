"""sch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index),
    path('profile', views.profile),
    path('register', views.register),
    path('login', views.log_in),
    path('logout', views.logout_),
    path('product/add_opinion/<str:product_type>/<str:title>', views.add_opinion),
    path('product/buy/<str:product_type>/<str:title>', views.product_buy),
    path('product/<str:product_type>/<str:title>/<int:rate>', views.leave_rate),
    path('product/<str:product_type>/<str:title>', views.product),
    path('product/<str:product_type>', views.product_list),
    path('admin/', admin.site.urls),
]
