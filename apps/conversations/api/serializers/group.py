from rest_framework import serializers
from apps.conversations.models import Group, GroupMember
from apps.users.models import User

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Replace with your User model
        fields = ['id',]  # Replace with the fields you want to include

class GroupCreationSerializer(serializers.ModelSerializer):
    friends_ids = MemberSerializer(many=True)
    class Meta:
        model = Group
        fields = ['id', 'name', 'friends_ids']