from django.shortcuts import render
from django.http import HttpResponse

TAG_LIST = [
    {
        'id': 0,
        'title': 'Рестораны',
        'src': 'http://127.0.0.1:9000/mapobject/0.jpg',
        'description': 'Здесь можно насладиться вкусной едой и приятной атмосферой'
    },
    {
        'id': 1,
        'title': 'Гостиницы',
        'src': 'http://127.0.0.1:9000/mapobject/1.jpg',
        'description': 'Уютные места для комфортного отдыха'
    },
    {
        'id': 2,
        'title': 'Развлечения',
        'src': 'http://127.0.0.1:9000/mapobject/2.jpg',
        'description': 'Места для активного времяпрепровождения'
    },
    {
        'id': 3,
        'title': 'Спорт',
        'src': 'http://127.0.0.1:9000/mapobject/3.jpg',
        'description': 'Для любителей активного образа жизни'
    },
    {
        'id': 4,
        'title': 'Медицина',
        'src': 'http://127.0.0.1:9000/mapobject/4.jpg',
        'description': 'Места для здоровья и ухода за собой'
    },
    {
        'id': 5,
        'title': 'Красота',
        'src': 'http://127.0.0.1:9000/mapobject/5.jpg',
        'description': 'Салоны красоты и ухода за внешностью'
    },
    {
        'id': 6,
        'title': 'Авто-сервисы',
        'src': 'http://127.0.0.1:9000/mapobject/6.jpg',
        'description': 'Для ремонта и обслуживания автомобилей'
    },
    {
        'id': 7,
        'title': 'Образование',
        'src': 'http://127.0.0.1:9000/mapobject/7.jpg',
        'description': 'Учебные заведения и курсы обучения'
    },
    {
        'id': 8,
        'title': 'Финансы',
        'src': 'http://127.0.0.1:9000/mapobject/8.jpg',
        'description': 'Сфера финансовых услуг'
    },
    {
        'id': 9, 'title': 'Туризм',
        'src': 'http://127.0.0.1:9000/mapobject/9.jpg',
        'description': 'Путешествия и туристические услуги'
    }]


def cart_list(items_count):
    return [
        {
            'id': TAG_LIST[i]['id'],
            'title':  TAG_LIST[i]['title'],
            'src':  TAG_LIST[i]['src'],
            'description': TAG_LIST[i]['description'],
            'is_main': i==1
        }for i in range(items_count-1)
    ]


CART = [
    {
        'id': 1,
        'address': 'jicdi',
        'name': f'jsjsja = {1}',
        'coordinate': 11,
        'description': 'kakaka',
        'cart_list': cart_list(10)
    },
    {
        'id': 2,
        'address': 'jicdi',
        'name': f'jsjsja = {2}',
        'coordinate': 22,
        'description': 'kakaka',
        'cart_list': cart_list(2)
    }
]

current_cart_id = 0
# Create your views here.
def tag_list(request):
    search_tag = request.GET.get('search_tag')
    if (search_tag is None):
        search_tag = ''
        tag_list= TAG_LIST
    else: tag_list = list(filter(lambda tag: tag['title'].lower().startswith(search_tag.lower()), TAG_LIST))
    count_cart_items = len(CART[current_cart_id]['cart_list'])
    return render(request, 'tag_list.html', {'tags': {'tag_list': tag_list,
                                                      'search_tag': search_tag,
                                                      'cart_count': count_cart_items,
                                                      'current_cart_id': current_cart_id}})


def tag(request, tag_id):
    tag_item = TAG_LIST[tag_id]
    return render(request, 'tag.html', {'tag': tag_item})


def cart(request, cart_id):
    cart_item = CART[cart_id]
    return render(request, 'cart.html', {'cart': cart_item})
