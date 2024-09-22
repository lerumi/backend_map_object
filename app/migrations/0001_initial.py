# Generated by Django 4.2.15 on 2024-09-22 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Objects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obj_name', models.CharField(max_length=30)),
                ('obj_description', models.TextField(blank=True)),
                ('obj_address', models.CharField(max_length=100)),
                ('obj_coordinates', models.CharField(max_length=30)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('formation_datetime', models.DateTimeField(blank=True, null=True)),
                ('completion_datetime', models.DateTimeField(blank=True, null=True)),
                ('obj_status', models.CharField(choices=[('Черновик', 'Draft'), ('Сформирован', 'Formed'), ('Завершен', 'Completed'), ('Удален', 'Deleted'), ('Отклонен', 'Rejected')])),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_objects', to=settings.AUTH_USER_MODEL)),
                ('moderator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='moderated_objects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=30)),
                ('tag_description', models.TextField()),
                ('tag_image', models.CharField(max_length=100)),
                ('tag_status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ObjectsTagsItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_main', models.BooleanField(default=False)),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.objects')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.tags')),
            ],
            options={
                'unique_together': {('object', 'tag')},
            },
        ),
    ]
