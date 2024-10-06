from app.models import Objects, ObjectsTagsItem, Tags, AuthUser
from rest_framework import serializers


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ["id", "tag_name", "tag_description", "tag_image", "tag_status"]
class ObjectsTagsItemSerializer(serializers.ModelSerializer):
    tag = TagsSerializer()
    class Meta:
        model = ObjectsTagsItem
        fields = ["id", "is_main", "object", "tag"]
class ObjectsSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    moderator = serializers.StringRelatedField()
    class Meta:
        model = Objects
        fields = ["id", "obj_name", "obj_description", "obj_address", "obj_coordinates", "creator", "moderator",
                  "creation_datetime", "formation_datetime", "completion_datetime", "obj_status"]

class ObjectSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    moderator = serializers.StringRelatedField()
    tags = ObjectsTagsItemSerializer(source='object_set', many=True, read_only=True)
    class Meta:
        model = Objects
        fields = ["id", "obj_name", "obj_description", "obj_address", "obj_coordinates", "creator", "moderator",
                  "creation_datetime", "formation_datetime", "completion_datetime", "obj_status", "tags"]
class UserSerializer(serializers.ModelSerializer):
    object_set = ObjectsSerializer(many=True, read_only=True)

    class Meta:
        model = AuthUser
        fields = ["id", "first_name", "last_name", "object_set"]
