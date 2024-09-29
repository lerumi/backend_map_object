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
from app.views import tag_list, add_tag_into_cart, tags_list_api
from app.views import tag, tag_api
from app.views import cart, delete_draft_cart, object_cart_api, one_object_api, save_creator, save_moderate
from app.views import objects_tags_item
from app.views import user_api, autentification, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tag_list, name='tags'),
    path('tag/<int:tag_id>', tag, name='tag'),
    path('cart/<int:cart_id>', cart, name='cart'),
    path('add_tag', add_tag_into_cart, name='add_tag'),
    path('delete_cart', delete_draft_cart, name='del_cart'),

    path('api/tags/', tags_list_api.as_view(), name='get_tags'),
    path('api/tag/<int:tag_id>', tag_api.as_view(), name='get_tag'),

    path('api/objects/', object_cart_api.as_view(), name='get_objects'),
    path('api/object/<int:object_id>', one_object_api.as_view(), name='get_object'),

    path('api/object/creator/<int:object_id>', save_creator, name='save_object_creator'),
    path('api/object/moderator/<int:object_id>', save_moderate, name='save_object_moderator'),

    path('api/object_item/<int:object_id>/<int:tag_id>', objects_tags_item.as_view(), name='object_item'),
    path('api/user/registr', user_api.as_view(), name='registr'),
    path('api/user/auth', autentification, name='auth'),
    path('api/user/logout', logout, name='logout')
]
