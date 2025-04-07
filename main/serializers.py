from rest_framework import serializers

from .models import BioItem, Contact, Project, Skill, User, UserProject, UserSkill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "skill_name"]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "project_name", "project_description"]


class BioItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BioItem
        fields = ["bio_item"]


class ContactSerializer(serializers.ModelSerializer):
    contact_type = serializers.StringRelatedField()

    class Meta:
        model = Contact
        fields = ["contact", "contact_type"]


class UserSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()
    contacts = ContactSerializer(many=True, read_only=True)

    def get_skills(self, obj):
        user_skills = UserSkill.objects.filter(user=obj).select_related("skill")
        return SkillSerializer([us.skill for us in user_skills], many=True).data

    def get_projects(self, obj):
        user_projects = UserProject.objects.filter(user=obj).select_related("project")
        return ProjectSerializer([up.project for up in user_projects], many=True).data

    def get_bio(self, obj):
        if hasattr(obj, "bio"):
            return BioItemSerializer(obj.bio).data
        return None

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "skills",
            "projects",
            "bio",
            "contacts",
        ]
