import phonenumbers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import URLValidator, validate_email
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import (
    BioItem,
    Candidate,
    CandidateProject,
    CandidateSkill,
    Contact,
    ContactType,
    Project,
    Skill,
)


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        validated_data["is_active"] = True
        return super().create(validated_data)


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ["id", "first_name", "last_name"]


class BioItemSerializer(serializers.ModelSerializer):
    candidate = serializers.PrimaryKeyRelatedField(queryset=Candidate.objects.all())

    class Meta:
        model = BioItem
        fields = ["id", "bio_item", "candidate"]

    def validate_candidate(self, value):
        if (
            BioItem.objects.filter(candidate=value)
            .exclude(id=self.instance.id if self.instance else None)
            .exists()
        ):
            raise ValidationError("This candidate already has a bio.")
        return value


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "skill_name"]


class CandidateSkillSerializer(serializers.ModelSerializer):
    candidate = serializers.PrimaryKeyRelatedField(queryset=Candidate.objects.all())
    skill = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all())

    class Meta:
        model = CandidateSkill
        fields = ["id", "skill", "candidate"]

    def create(self, validated_data):
        candidate = validated_data["candidate"]
        skill = validated_data["skill"]

        candidate_skill, created = CandidateSkill.objects.get_or_create(
            candidate=candidate, skill=skill
        )

        return candidate_skill


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "project_name", "project_description"]


class CandidateProjectSerializer(serializers.ModelSerializer):
    candidate = serializers.PrimaryKeyRelatedField(queryset=Candidate.objects.all())
    project = ProjectSerializer()

    class Meta:
        model = CandidateProject
        fields = ["id", "project", "candidate"]

    def create(self, validated_data):
        candidate_id = validated_data.pop("candidate")
        project_data = validated_data.pop("project")

        project, created = Project.objects.get_or_create(
            project_name=project_data.get("project_name"),
            project_description=project_data.get("project_description"),
        )

        candidate_project = CandidateProject.objects.create(
            candidate=candidate_id, project=project
        )

        return candidate_project


class ContactSerializer(serializers.ModelSerializer):
    candidate = serializers.PrimaryKeyRelatedField(
        queryset=Candidate.objects.all(), required=False
    )

    contact_type = serializers.PrimaryKeyRelatedField(
        queryset=ContactType.objects.all()
    )

    class Meta:
        model = Contact
        fields = ["id", "candidate", "contact_type", "contact"]

    def validate_contact(self, value):
        contact_type = self.initial_data.get("contact_type")
        if contact_type:
            try:
                contact_type_obj = ContactType.objects.get(pk=contact_type)
                contact_type_name = contact_type_obj.contact_type.lower()

                if contact_type_name == "email":
                    try:
                        validate_email(value)
                    except DjangoValidationError:
                        raise ValidationError(
                            "The contact field must contain a valid email address."
                        )

                elif contact_type_name == "phone":
                    try:
                        phone_number = phonenumbers.parse(value, None)
                        if not phonenumbers.is_valid_number(phone_number):
                            raise ValidationError(
                                "The contact field must contain a valid phone number."
                            )
                    except phonenumbers.NumberParseException:
                        raise ValidationError(
                            "The contact field must contain a valid phone number."
                        )

                elif contact_type_name == "profile":
                    url_validator = URLValidator()
                    try:
                        url_validator(value)
                    except DjangoValidationError:
                        raise ValidationError(
                            "The contact field must contain a valid URL."
                        )

            except ContactType.DoesNotExist:
                raise ValidationError("Invalid contact type provided.")
        return value


class ContactTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactType
        fields = ["id", "contact_type"]


class CandidateSummarySerializer(serializers.ModelSerializer):
    bio = BioItemSerializer()
    skills = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    contacts = ContactSerializer(many=True, read_only=True)

    def get_skills(self, obj):
        candidate_skills = CandidateSkill.objects.filter(candidate=obj).select_related(
            "skill"
        )
        return SkillSerializer([us.skill for us in candidate_skills], many=True).data

    def get_projects(self, obj):
        candidate_projects = CandidateProject.objects.filter(
            candidate=obj
        ).select_related("project")
        return ProjectSerializer(
            [up.project for up in candidate_projects], many=True
        ).data

    def get_bio(self, obj):
        if hasattr(obj, "bio"):
            return BioItemSerializer(obj.bio).data
        return None

    class Meta:
        model = Candidate
        fields = [
            "id",
            "first_name",
            "last_name",
            "bio",
            "skills",
            "projects",
            "contacts",
        ]
