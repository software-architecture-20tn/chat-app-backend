from django.db.models import Q

from rest_framework import serializers

from drf_spectacular.utils import extend_schema_field

from apps.conversations.models import Group, GroupAdmin, GroupMember
from apps.users.models import Friendship, User


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
        )


class GroupSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "members",
        )

    @extend_schema_field(MemberSerializer(many=True))
    def get_members(self, group):
        """Get the members of the group."""
        members = group.members.all()
        users = [
            member.member
            for member in members
        ]
        return MemberSerializer(users, many=True).data


class GroupCreationSerializer(serializers.ModelSerializer):
    friend_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
    )
    members = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "friend_ids",
            "members",
        )

    def validate(self, attrs):
        """Validate the friend_ids field."""
        friend_ids = attrs.get("friend_ids")
        if not friend_ids:
            raise serializers.ValidationError(
                {"message": "You must specify friends to create a new group"},
            )
        friends = Friendship.objects.filter(
            Q(user1=self.context["request"].user, user2__in=friend_ids)
            | Q(user2=self.context["request"].user, user1__in=friend_ids)
        ).values_list("user1", "user2")
        if len(friends) < len(friend_ids):
            raise serializers.ValidationError(
                {"message": "Some users are not your friends"},
            )
        return super().validate(attrs)

    def create(self, validated_data):
        friends = validated_data.pop("friend_ids")
        validated_data["person_created"] = self.context["request"].user
        group = super().create(validated_data)

        if not group:
            return None

        GroupAdmin.objects.create(
            admin=self.context["request"].user,
            group=group,
        )
        for friend in friends:
            GroupMember.objects.create(
                member=friend,
                group=group,
            )
        return group

    @extend_schema_field(MemberSerializer(many=True))
    def get_members(self, group):
        """Get the members of the group."""
        members = group.members.all()
        users = [
            member.member
            for member in members
        ]
        return MemberSerializer(users, many=True).data
