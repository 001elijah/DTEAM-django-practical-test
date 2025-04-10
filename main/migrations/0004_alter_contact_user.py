# Generated by Django 4.2.20 on 2025-04-06 19:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_remove_project_user_remove_skill_user_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contacts",
                to="main.user",
            ),
        ),
    ]
