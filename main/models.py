from django.contrib.auth.models import User
from django.db import models


class Candidate(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_candidates",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class BioItem(models.Model):
    bio_item = models.TextField()
    candidate = models.OneToOneField(
        Candidate, on_delete=models.CASCADE, related_name="bio"
    )

    def __str__(self):
        return f"Bio of {self.candidate.first_name} {self.candidate.last_name}"


class Skill(models.Model):
    skill_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.skill_name


class CandidateSkill(models.Model):
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="candidate_skills"
    )
    skill = models.ForeignKey(
        Skill, on_delete=models.CASCADE, related_name="candidate_skills"
    )


class Project(models.Model):
    project_name = models.CharField(max_length=255)
    project_description = models.TextField()

    def __str__(self):
        return self.project_name


class CandidateProject(models.Model):
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="candidate_projects"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="candidate_projects"
    )


class ContactType(models.Model):
    contact_type = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.contact_type


class Contact(models.Model):
    contact = models.CharField(max_length=255, unique=True)
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="contacts"
    )
    contact_type = models.ForeignKey(
        ContactType, on_delete=models.CASCADE, related_name="contacts"
    )

    def __str__(self):
        return (
            f"{self.contact_type.contact_type}: {self.contact} "
            f"({self.candidate.first_name} {self.candidate.last_name})"
        )
