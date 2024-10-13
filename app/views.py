import uuid

from django.utils import timezone
from django.db import connection
from django.shortcuts import render, redirect
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .models import Tags, Objects, ObjectsTagsItem, CustomUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from app.serializers import TagsSerializer, ObjectsSerializer, ObjectsTagsItemSerializer, ObjectSerializer, CustomUserSerializer
from django.contrib.auth import get_user_model
from .minio import *
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q
from rest_framework.filters import OrderingFilter
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from django.views.decorators.csrf import csrf_exempt
from app.permission import IsManager, IsSimpleUser, AuthBySessionID
from app.redis import session_storage
class UserViewSet(viewsets.ModelViewSet):
    """Класс, описывающий методы работы с пользователями
    Осуществляет связь с таблицей пользователей в базе данных
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    model_class = CustomUser
    def create(self, request):
        """
        Функция регистрации новых пользователей
        Если пользователя c указанным в request email ещё нет, в БД будет добавлен новый пользователь.
        """
        if self.model_class.objects.filter(email=request.data['email']).exists():
            return Response({'status': 'Exist'}, status=400)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            self.model_class.objects.create_user(email=serializer.data['email'],
                                     password=serializer.data['password'],
                                     is_superuser=serializer.data['is_superuser'],
                                     is_staff=serializer.data['is_staff'])
            return Response({'status': 'Success'}, status=200)
        return Response({'status': 'Error', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes
            self.check_permissions(self.request)
            self.perform_authentication(self.request)
            return func(self, *args, **kwargs)
        return decorated_func
    return decorator
@csrf_exempt
@swagger_auto_schema(method='post', request_body=CustomUserSerializer)
@permission_classes([AllowAny])
@authentication_classes([])
@api_view(['Post'])
def login_view(request):
    username = request.data["email"]
    password = request.data["password"]
    user = authenticate(request, email=username, password=password)
    if user is not None:
        random_key = str(uuid.uuid4())
        session_storage.set(random_key, username)
        response_data = {
            'status': 'ok',
            'session_id': random_key
        }
        response = Response(response_data, status=status.HTTP_201_CREATED)
        response.set_cookie("session_id", random_key, samesite="lax")
        return response
    else:
        return HttpResponse("{'status': 'error', 'error': 'login failed'}")

def logout_view(request):
    logout(request._request)
    return Response({'status': 'Success'})

def tag_list(request):
    user1 = CustomUser.objects.get(id = request.user.id)
    search_tag = request.GET.get('search_tag')
    if (search_tag is None):
        search_tag = ''
        tag_list= Tags.objects.filter(tag_status=True)
    else: tag_list = Tags.objects.filter(tag_name__icontains=search_tag, tag_status=True)
    if(user1.created_objects.filter(obj_status="Черновик").first()!= None):
        current_object = user1.created_objects.get(obj_status="Черновик")
        current_object_id = current_object.id
        count_object_items = ObjectsTagsItem.objects.filter(object=current_object).count()
    else:
        count_object_items = 0
        current_object_id = 0
    return render(request, 'tag_list.html', {'tags': {'tag_list': tag_list,
                                                      'search_tag': search_tag,
                                                      'object_count': count_object_items,
                                                      'current_object_id': current_object_id}})
def tag(request, tag_id):
    tag_item = Tags.objects.get(id=tag_id)
    return render(request, 'tag.html', {'tag': tag_item})

def object(request, object_id):
    object_item = Objects.objects.get(id=object_id)
    if(Objects.objects.get(id=object_id).obj_status=="Удален"):
        return redirect('tags')
    tag_items = Tags.objects.filter(tag_set__object = object_item)
    return render(request, 'cart.html', {'object': object_item, 'object_tags_list': tag_items})

def add_tag_into_object(request):
    user1 = CustomUser.objects.get(id = request.user.id)
    tag_id = request.POST.get('tag_id')
    tag = Tags.objects.get(id=tag_id)
    user_object, created = Objects.objects.get_or_create(creator=user1, obj_status="Черновик")
    adding_tag_to_object, created = ObjectsTagsItem.objects.get_or_create(tag=tag, object=user_object)
    adding_tag_to_object.save()
    user_object.save()
    return redirect('tags')
def delete_draft_object(request):
    object_id = request.POST.get('object_id')
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE app_objects
            SET obj_status = 'Удален'
            WHERE id = %s
        """, [object_id])
    return redirect('tags')


class tags_list_api(APIView):
    authentication_classes = [AuthBySessionID]
    permission_classes = [IsManager | IsSimpleUser]
    model_class = Tags
    serializer_class = TagsSerializer

    @method_permission_classes((AllowAny,))
    def get(self, request, format=None):
        user1 = CustomUser.objects.get(id = request.user.id)
        search_tag = request.query_params.get('search_tag')
        if (search_tag is None):
            search_tag = ''
            tag_list = self.model_class.objects.filter(tag_status=True)
        else:
            tag_list =  self.model_class.objects.filter(tag_name__icontains=search_tag, tag_status=True)
        if (user1.created_objects.filter(obj_status="Черновик").first() != None):
            current_object = user1.created_objects.get(obj_status="Черновик")
            current_object_id = current_object.id
            count_object_items = ObjectsTagsItem.objects.filter(object=current_object).count()
        else:
            count_object_items = 0
            current_object_id = 0
        serializer = self.serializer_class(tag_list, many=True)
        return Response({'tags': serializer.data, 'current object id': current_object_id, 'count object items': count_object_items})

    @swagger_auto_schema(request_body=TagsSerializer)
    @method_permission_classes((IsManager, ))
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='post', request_body=TagsSerializer)
@api_view(['post'])
@permission_classes([IsManager])
@authentication_classes([])
def image_add(request, tag_id, format=None):
    tag, created = Tags.objects.get_or_create(id=tag_id)
    pic = request.FILES.get('tag_image')
    result = add_pic(tag, pic)
    if created:
        tag.delete()
    if 'error' in result.data:
        return result
    return Response(status=status.HTTP_200_OK)
class tag_api(APIView):
    model_class = Tags
    serializer_class = TagsSerializer
    authentication_classes = [AuthBySessionID]
    permission_classes = [IsManager | IsSimpleUser]

    @method_permission_classes((AllowAny,))
    def get(self, request, tag_id, format=None):
        tag = get_object_or_404(self.model_class, id=tag_id)
        serializer = self.serializer_class(tag)
        return Response(serializer.data)


    @swagger_auto_schema(request_body=TagsSerializer)
    @method_permission_classes([IsManager])
    def put(self, request, tag_id, format=None):
        tag = get_object_or_404(self.model_class, id=tag_id)
        serializer = self.serializer_class(tag, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes([IsManager | IsSimpleUser])
    @swagger_auto_schema(request_body=ObjectsTagsItemSerializer)
    def post(self, request, tag_id, format=None):
        user1 = CustomUser.objects.get(id = request.user.id)
        user_object, created = Objects.objects.get_or_create(creator=user1, obj_status="Черновик")
        tag = get_object_or_404(self.model_class, id=tag_id)
        user_object.save()
        if not (ObjectsTagsItem.objects.filter(tag=tag, object=user_object).first()):
            new_object_tag = ObjectsTagsItem.objects.create(tag=tag, object=user_object)
            new_object_tag.save()
            return Response(ObjectsTagsItemSerializer(new_object_tag).data, status=status.HTTP_200_OK)
        return Response({'Предупреждение': 'Данный тег уже в заявке'},status=status.HTTP_208_ALREADY_REPORTED)

    @method_permission_classes((IsManager,))
    def delete(self, request, tag_id, format=None):
        tag = get_object_or_404(self.model_class, id=tag_id)
        tags = ObjectsTagsItem.objects.filter(tag = tag_id)
        for one_tag in tags:
            one_tag.delete()
        tag.delete()
        del_pic(tag_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
class object_cart_api(APIView):
    model_class = Objects
    serializer_class = ObjectsSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, AuthBySessionID]
    permission_classes = [IsManager | IsSimpleUser]

    @method_permission_classes([IsSimpleUser | IsManager])
    def get(self, request, format=None):
        user1 = CustomUser.objects.get(id = request.user.id)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        status_1 = request.query_params.get('status')
        if user1.is_staff:
            object_list = self.model_class.objects
        else:
            object_list = user1.created_objects.exclude(obj_status="Черновик").exclude(obj_status="Удален")
        if start_date or end_date:
            if not (start_date):
                object_list = object_list.filter(formation_datetime__lte=end_date)
            elif not(end_date):
                object_list = object_list.filter(formation_datetime__gte= start_date)
            else:
                object_list = object_list.filter(formation_datetime__range=[start_date, end_date])
        if status_1:
            object_list = object_list.filter(obj_status=status_1)
        if not (object_list):
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(object_list, many=True)
            return Response(serializer.data)
class one_object_api(APIView):
    model_class = Objects
    serializer_class = ObjectSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, AuthBySessionID]
    permission_classes = [IsManager | IsSimpleUser]

    @method_permission_classes([IsManager | IsSimpleUser])
    def get(self, request, object_id, format=None):
        object = get_object_or_404(self.model_class, id=object_id)
        serializer = self.serializer_class(object)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ObjectSerializer)
    @method_permission_classes([IsManager | IsSimpleUser])
    def put(self, request, object_id, format=None):
        object = get_object_or_404(self.model_class, id=object_id)
        serializer = self.serializer_class(object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes((IsSimpleUser,))
    def delete(self, request, object_id, format=None):
        object = get_object_or_404(self.model_class, id=object_id)
        object.obj_status = "Удален"
        object.completion_datetime = timezone.now()
        object.save()
        serializer = self.serializer_class(object)
        return Response({'Успешно': 'Объект переведен в статус '"'Удален'"'.', 'Объект:':serializer.data},status=status.HTTP_204_NO_CONTENT)

@api_view(['put'])
@authentication_classes([AuthBySessionID])
@permission_classes((IsSimpleUser, ))
def save_creator(request, object_id, format=None):
    object = get_object_or_404(Objects, id=object_id)
    serialized = ObjectsSerializer(object)
    main_tag = object.object_set.filter(is_main="True").first()
    if(object.obj_status != "Черновик"):
        return Response({'Ошибка': 'Не хватает прав для редактирования.'}, status=status.HTTP_403_FORBIDDEN)
    if object.obj_name != "" and object.obj_description != "" and object.obj_address != "" and object.obj_coordinates != "":
        if( main_tag is None):
            return Response({'Ошибка': 'Не выбран главный тег!'}, status=status.HTTP_400_BAD_REQUEST)
        object.formation_datetime = timezone.now()
        object.obj_status = "Сформирован"
        object.save()
        return Response(serialized.data, status=status.HTTP_200_OK)
    return Response({'Ошибка': 'Какое-то из полей не заполнено.'}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['put'])
@authentication_classes([AuthBySessionID])
@permission_classes([IsManager])
def save_moderate(request, object_id, format=None):
    accepted = request.data.get('accept')
    object = get_object_or_404(Objects, id=object_id)
    serialized = ObjectSerializer(object)
    if(object.obj_status == "Черновик"):
        return Response({'Ошибка': 'Нельзя модерировать черновики.'}, status=status.HTTP_400_BAD_REQUEST)
    if accepted == 'True':
        object.obj_status = "Завершен"
    else:
        object.obj_status = "Отклонен"
    object.completion_datetime = timezone.now()
    print(request.user.id)
    object.moderator = CustomUser.objects.filter(id = request.user.id).first()
    object.save()
    return Response(serialized.data, status=status.HTTP_202_ACCEPTED)

class objects_tags_item(APIView):
    model_class = ObjectsTagsItem
    serializer_class = ObjectsTagsItemSerializer
    authentication_classes = [AuthBySessionID]
    permission_classes = [IsManager | IsSimpleUser]

    @method_permission_classes([IsManager | IsSimpleUser])
    def delete(self, request, tag_id, object_id, format=None):
        deleted_tag = get_object_or_404(self.model_class, object=object_id, tag=tag_id)
        deleted_tag.delete()
        return Response(status=status.HTTP_202_ACCEPTED)

    @method_permission_classes([IsManager | IsSimpleUser])
    def put(self, request, tag_id, object_id, format=None):
        edited_tag = get_object_or_404(self.model_class, object=object_id, tag=tag_id)
        main_tag = request.data.get('is_main')
        if main_tag == 'True':
            object =self.model_class.objects.filter(object=object_id)
            prev_main_tag = object.filter(is_main=True)
            for one_tag in prev_main_tag:
                one_tag.is_main = False
                one_tag.save()
            edited_tag.is_main = True
        else:
            edited_tag.is_main = False
        edited_tag.save()
        return Response(status=status.HTTP_202_ACCEPTED)




