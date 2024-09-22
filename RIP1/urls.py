"""
URL configuration for RIP1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from app.views import tag_list, add_tag_into_cart
from app.views import tag
from app.views import cart, delete_draft_cart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tag_list, name='tags'),
    path('tag/<int:tag_id>', tag, name='tag'),
    path('cart/<int:cart_id>', cart, name='cart'),
    path('add_tag', add_tag_into_cart, name='add_tag'),
    path('delete_cart', delete_draft_cart, name='del_cart')
]
