# Generated by Django 5.2 on 2025-04-06 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CV",
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
                ("firstname", models.CharField(max_length=50)),
                ("lastname", models.CharField(max_length=50)),
                ("skills", models.TextField()),
                ("projects", models.TextField()),
                ("bio", models.TextField()),
                ("contacts", models.TextField()),
            ],
        ),
    ]
