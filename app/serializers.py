from app.models import Objects, ObjectsTagsItem, Tags, CustomUser
from rest_framework import serializers
from collections import OrderedDict


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ["id", "tag_name", "tag_description", "tag_image", "tag_status"]

        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields
class ObjectsTagsItemSerializer(serializers.ModelSerializer):
    tag = TagsSerializer()
    class Meta:
        model = ObjectsTagsItem
        fields = ["id", "is_main", "object", "tag"]

        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields
class ObjectsSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    moderator = serializers.StringRelatedField()
    class Meta:
        model = Objects
        fields = ["id", "obj_name", "obj_description", "obj_address", "obj_coordinates", "creator", "moderator",
                  "creation_datetime", "formation_datetime", "completion_datetime", "obj_status"]

        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields
class ObjectSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    moderator = serializers.StringRelatedField()
    tags = ObjectsTagsItemSerializer(source='object_set', many=True, read_only=True)
    class Meta:
        model = Objects
        fields = ["id", "obj_name", "obj_description", "obj_address", "obj_coordinates", "creator", "moderator",
                  "creation_datetime", "formation_datetime", "completion_datetime", "obj_status", "tags"]

        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields

class CustomUserSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(default=False, required=False)
    is_superuser = serializers.BooleanField(default=False, required=False)
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'is_staff', 'is_superuser']
        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields