# Generated by Django 4.2.5 on 2023-11-07 13:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_user_username"),
    ]

    operations = [
        migrations.CreateModel(
            name="Friendship",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("date", models.DateField(auto_now_add=True)),
                ("is_close", models.BooleanField(default=False)),
                (
                    "user1",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="friendship_user1",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User 1",
                    ),
                ),
                (
                    "user2",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="friendship_user2",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User 2",
                    ),
                ),
            ],
            options={
                "verbose_name": "Friendship",
                "verbose_name_plural": "Friendships",
                "unique_together": {("user1", "user2")},
            },
        ),
        migrations.CreateModel(
            name="FriendRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "date_time_sent",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Date and time sent"
                    ),
                ),
                (
                    "is_approved",
                    models.BooleanField(default=False, verbose_name="Approved"),
                ),
                (
                    "receiver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="friend_request_received",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Receiver",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="friend_request_sent",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Sender",
                    ),
                ),
            ],
            options={
                "verbose_name": "Friend request",
                "verbose_name_plural": "Friend requests",
                "unique_together": {("sender", "receiver")},
            },
        ),
    ]
