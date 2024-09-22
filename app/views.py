from datetime import datetime
from django.db import connection
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Tags, Objects, ObjectsTagsItem

def tag_list(request):
    search_tag = request.GET.get('search_tag')
    if (search_tag is None):
        search_tag = ''
        tag_list= Tags.objects.filter(tag_status=True)
    else: tag_list = Tags.objects.filter(tag_name__icontains=search_tag, tag_status=True)
    try:
        current_cart = request.user.created_objects.get(obj_status="Черновик")
        current_cart_id = current_cart.id
        count_cart_items = ObjectsTagsItem.objects.filter(object=current_cart).count()
    except:
        count_cart_items = 0
        current_cart_id = 0
    return render(request, 'tag_list.html', {'tags': {'tag_list': tag_list,
                                                      'search_tag': search_tag,
                                                      'cart_count': count_cart_items,
                                                      'current_cart_id': current_cart_id}})
def tag(request, tag_id):
    tag_item = Tags.objects.get(id=tag_id)
    return render(request, 'tag.html', {'tag': tag_item})

def cart(request, cart_id):
    cart_item = Objects.objects.get(id=cart_id)
    tag_items = Tags.objects.filter(objectstagsitem__object = cart_item)
    return render(request, 'cart.html', {'cart': cart_item, 'cart_tags_list': tag_items})

def add_tag_into_cart(request):
    tag_id = request.POST.get('tag_id')
    tag = Tags.objects.get(id=tag_id)
    user_cart, created = Objects.objects.get_or_create(creator=request.user, obj_status="Черновик")
    adding_tag_to_cart, created = ObjectsTagsItem.objects.get_or_create(tag=tag, object=user_cart)
    adding_tag_to_cart.save()
    user_cart.save()
    return redirect('tags')
def delete_draft_cart(request):
    cart_id = request.POST.get('cart_id')
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE app_objects
            SET obj_status = 'Удален'
            WHERE id = %s
        """, [cart_id])
    return redirect('tags')