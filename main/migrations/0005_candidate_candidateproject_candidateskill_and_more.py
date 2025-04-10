# Generated by Django 4.2.20 on 2025-04-07 17:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0004_alter_contact_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="Candidate",
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
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_candidates",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CandidateProject",
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
                (
                    "candidate",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="candidate_projects",
                        to="main.candidate",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="candidate_projects",
                        to="main.project",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CandidateSkill",
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
                (
                    "candidate",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="candidate_skills",
                        to="main.candidate",
                    ),
                ),
                (
                    "skill",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="candidate_skills",
                        to="main.skill",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="userproject",
            name="project",
        ),
        migrations.RemoveField(
            model_name="userproject",
            name="user",
        ),
        migrations.RemoveField(
            model_name="userskill",
            name="skill",
        ),
        migrations.RemoveField(
            model_name="userskill",
            name="user",
        ),
        migrations.RemoveField(
            model_name="bioitem",
            name="user",
        ),
        migrations.RemoveField(
            model_name="contact",
            name="user",
        ),
        migrations.DeleteModel(
            name="User",
        ),
        migrations.DeleteModel(
            name="UserProject",
        ),
        migrations.DeleteModel(
            name="UserSkill",
        ),
        migrations.AddField(
            model_name="bioitem",
            name="candidate",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bio",
                to="main.candidate",
            ),
        ),
        migrations.AddField(
            model_name="contact",
            name="candidate",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contacts",
                to="main.candidate",
            ),
        ),
    ]
