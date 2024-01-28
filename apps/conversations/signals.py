from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Group, GroupMember


@receiver(post_save, sender=Group)
def create_a_group_member_instance_for_the_creator(
    instance: Group,
    created: bool,
    **kwargs,
) -> None:
    """Create a group member instance for the creator of the group."""
    if not created:
        return
    GroupMember.objects.create(
        group=instance,
        member=instance.person_created,  # type: ignore
    )
