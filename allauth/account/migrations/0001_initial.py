# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

from pgcrypto.fields import CharPGPSymmetricKeyField
from entities.models.entities import Entity

UNIQUE_EMAIL = getattr(settings, "ACCOUNT_UNIQUE_EMAIL", True)


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="EmailAddress",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "email",
                    CharPGPSymmetricKeyField(
                        unique=UNIQUE_EMAIL,
                        max_length=75,
                        verbose_name="email address",
                    ),
                ),
                (
                    'alias',
                    models.CharField(
                        blank=True, 
                        max_length=50, 
                        verbose_name='Alias'
                    ),
                ),
                (
                    "verified",
                    models.BooleanField(default=False, verbose_name="verified"),
                ),
                (
                    "primary",
                    models.BooleanField(default=False, verbose_name="primary"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        verbose_name="user",
                        to=settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    'entity',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='entity_email',
                        to='entities.entity',
                        verbose_name='entity'
                    ),
                ),
            ],
            options={
                "db_table": 'ent_email_addresses',
                "verbose_name": "email address",
                "verbose_name_plural": "email addresses",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="EmailConfirmation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="created",
                    ),
                ),
                ("sent", models.DateTimeField(null=True, verbose_name="sent")),
                (
                    "key",
                    models.CharField(unique=True, max_length=64, verbose_name="key"),
                ),
                (
                    "email_address",
                    models.ForeignKey(
                        verbose_name="email address",
                        to="account.EmailAddress",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "verbose_name": "email confirmation",
                "verbose_name_plural": "email confirmations",
            },
            bases=(models.Model,),
        ),
    ]

    if not UNIQUE_EMAIL:
        operations += [
            migrations.AlterUniqueTogether(
                name="emailaddress",
                unique_together=set([("user", "email")]),
            ),
        ]
