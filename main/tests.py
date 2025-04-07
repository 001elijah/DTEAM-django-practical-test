from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from main.models import (
    BioItem,
    Contact,
    ContactType,
    Project,
    Skill,
    User,
    UserProject,
    UserSkill,
)


class CVViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(first_name="John", last_name="Doe")

        self.skill_python = Skill.objects.create(skill_name="Python")
        self.skill_django = Skill.objects.create(skill_name="Django")
        UserSkill.objects.create(user=self.user, skill=self.skill_python)
        UserSkill.objects.create(user=self.user, skill=self.skill_django)

        self.project_portfolio = Project.objects.create(
            project_name="Portfolio",
            project_description="A sample portfolio project",
        )
        UserProject.objects.create(user=self.user, project=self.project_portfolio)

        self.bio = BioItem.objects.create(
            user=self.user, bio_item="Experienced Software Developer"
        )

        self.email_type = ContactType.objects.create(contact_type="Email")
        self.phone_type = ContactType.objects.create(contact_type="Phone")
        self.email_contact = Contact.objects.create(
            user=self.user, contact="john.doe@example.com", contact_type=self.email_type
        )
        self.phone_contact = Contact.objects.create(
            user=self.user, contact="123-456-7890", contact_type=self.phone_type
        )

    def test_cv_list_view(self):
        """
        Test the CV list view to ensure it returns the correct list of users.
        """
        response = self.client.get(reverse("cv_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Doe")

    def test_cv_detail_view(self):
        """
        Test the CV detail view to ensure it loads all user-related data including
        skills, projects, bio, and contacts correctly.
        """
        response = self.client.get(reverse("cv_detail", args=[self.user.id]))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Experienced Software Developer")

        self.assertContains(response, "Python")
        self.assertContains(response, "Django")

        self.assertContains(response, "Portfolio")
        self.assertContains(response, "A sample portfolio project")

        self.assertContains(response, "john.doe@example.com")
        self.assertContains(response, "123-456-7890")


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(first_name="John", last_name="Doe")

    def test_list_users(self):
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_user(self):
        response = self.client.get(f"/users/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "John")

    def test_create_user(self):
        data = {"first_name": "Jane", "last_name": "Smith"}
        response = self.client.post("/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_user(self):
        data = {"first_name": "Johnny"}
        response = self.client.patch(f"/users/{self.user.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Johnny")

    def test_delete_user(self):
        response = self.client.delete(f"/users/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())
