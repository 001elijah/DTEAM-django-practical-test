from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Skill(models.Model):
    skill_name = models.CharField(
        max_length=100, unique=True
    )  # Ensures skills are unique

    def __str__(self):
        return self.skill_name


class Project(models.Model):
    project_name = models.CharField(max_length=255, unique=True)
    project_description = models.TextField()

    def __str__(self):
        return self.project_name


class BioItem(models.Model):
    bio_item = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="bio")

    def __str__(self):
        return f"Bio of {self.user.first_name} {self.user.last_name}"


class ContactType(models.Model):
    contact_type = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.contact_type


class Contact(models.Model):
    contact = models.CharField(
        max_length=255, unique=True
    )  # Ensure each contact is unique
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="contacts"
    )  # Allows multiple contacts per user
    contact_type = models.ForeignKey(
        ContactType, on_delete=models.CASCADE, related_name="contacts"
    )

    def __str__(self):
        return (
            f"{self.contact_type.contact_type}: {self.contact} "
            f"({self.user.first_name} {self.user.last_name})"
        )


class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_skills")
    skill = models.ForeignKey(
        Skill, on_delete=models.CASCADE, related_name="user_skills"
    )


class UserProject(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_projects"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="user_projects"
    )
