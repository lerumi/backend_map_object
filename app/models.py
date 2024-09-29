from django.db import models

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'auth_user'


class Tags(models.Model):
    tag_name = models.CharField(max_length=30)
    tag_description = models.TextField()
    tag_image = models.CharField(max_length=100)
    tag_status = models.BooleanField(default=True)
class Objects(models.Model):
    class ObjectStatus(models.TextChoices):
        DRAFT = "Черновик"
        FORMED = "Сформирован"
        COMPLETED = "Завершен"
        DELETED = "Удален"
        REJECTED = "Отклонен"
    obj_name = models.CharField(max_length=30, null=False)
    obj_description = models.TextField(blank=True, null=False)
    obj_address = models.CharField(max_length=100, null=False)
    obj_coordinates = models.CharField(max_length=30, null=False)
    creator = models.ForeignKey(AuthUser, on_delete=models.DO_NOTHING, related_name='created_objects')
    moderator = models.ForeignKey(AuthUser, on_delete=models.DO_NOTHING, related_name='moderated_objects', blank=True, null=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    formation_datetime = models.DateTimeField(blank=True, null=True)
    completion_datetime = models.DateTimeField(blank=True, null=True)

    obj_status = models.CharField(choices=ObjectStatus.choices)
# Create your models here.
class ObjectsTagsItem(models.Model):
    is_main = models.BooleanField(default=False)
    object = models.ForeignKey(Objects, on_delete=models.DO_NOTHING, related_name='object_set')
    tag = models.ForeignKey(Tags, on_delete=models.DO_NOTHING, related_name='tag_set')

    class Meta:
        unique_together = ('object', 'tag')