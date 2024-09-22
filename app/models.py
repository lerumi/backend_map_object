from django.db import models
from django.contrib.auth.models import User
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
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_objects')
    moderator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='moderated_objects', blank=True, null=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    formation_datetime = models.DateTimeField(blank=True, null=True)
    completion_datetime = models.DateTimeField(blank=True, null=True)

    obj_status = models.CharField(choices=ObjectStatus.choices)
# Create your models here.
class ObjectsTagsItem(models.Model):
    is_main = models.BooleanField(default=False)
    object = models.ForeignKey(Objects, on_delete=models.DO_NOTHING)
    tag = models.ForeignKey(Tags, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('object', 'tag')