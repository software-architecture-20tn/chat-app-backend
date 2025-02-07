from django.db.models import Q

from rest_framework import serializers

from drf_spectacular.utils import extend_schema_field

from apps.conversations.models import Group, GroupAdmin, GroupMember
from apps.core.api.serializers import BaseModelSerializer
from apps.users.models import Friendship, User


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "avatar",
        )


class GroupSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    admins = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "members",
            "admins",
        )

    @extend_schema_field(MemberSerializer(many=True))
    def get_members(self, group):
        """Get the members of the group."""
        members = group.members.all()
        users = [member.member for member in members]
        return MemberSerializer(users, many=True).data

    @extend_schema_field(MemberSerializer(many=True))
    def get_admins(self, group):
        """Get the admins of the group."""
        admins = group.admins.all()
        users = [admin.admin for admin in admins]
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
        """Create a new group.

        Create a new group with the name and friends (at least 1).

        """
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
        users = [member.member for member in members]
        return MemberSerializer(users, many=True).data


class GroupAddMemberSerializer(BaseModelSerializer):
    """Serializer for adding members to a group."""

    members_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
    )

    class Meta:
        model = Group
        fields = ("members_ids",)

    def validate(self, attrs):
        """Validate the members_ids field."""
        members_ids = attrs.get("members_ids")
        if not members_ids:
            raise serializers.ValidationError(
                {"message": "You must specify members to add to the group"},
            )
        friends = Friendship.objects.filter(
            Q(user1=self.context["request"].user, user2__in=members_ids)
            | Q(user2=self.context["request"].user, user1__in=members_ids)
        ).values_list("user1", "user2")
        if len(friends) < len(members_ids):
            raise serializers.ValidationError(
                {"message": "Some users are not your friends"},
            )
        return attrs

    def save(self, **kwargs):
        """Add members to the group."""
        members = self.validated_data.get("members_ids")
        group = self.instance
        for member in members:
            if not GroupMember.objects.filter(
                group=group,
                member=member,
            ).exists():
                GroupMember.objects.create(
                    group=group,
                    member=member,
                )
        return self.instance


class GroupRemoveMemberSerializer(BaseModelSerializer):
    """Serializer for adding members to a group."""

    members_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
    )

    class Meta:
        model = Group
        fields = ("members_ids",)

    def save(self, **kwargs):
        """Add members to the group."""
        members = self.validated_data.get("members_ids")
        group = self.instance
        for member in members:
            if GroupMember.objects.filter(
                group=group,
                member=member,
            ).exists():
                GroupMember.objects.filter(
                    group=group,
                    member=member,
                ).delete()
        return self.instance
