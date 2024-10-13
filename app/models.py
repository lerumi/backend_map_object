from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, BaseUserManager
from django.contrib.auth.models import Group, Permission


class NewUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email адрес", unique=True, max_length=254)
    password = models.CharField(max_length=100, verbose_name="Пароль")
    is_staff = models.BooleanField(default=False, verbose_name="Является ли пользователь менеджером?")
    is_superuser = models.BooleanField(default=False, verbose_name="Является ли пользователь админом?")

    USERNAME_FIELD = 'email'

    objects = NewUserManager()
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  # Unique related_name to avoid clashes
        blank=True,
        verbose_name='Группы'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Unique related_name to avoid clashes
        blank=True,
        verbose_name='Разрешения'
    )

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
    creator = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='created_objects')
    moderator = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='moderated_objects', blank=True, null=True)
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