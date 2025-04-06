from django.test import TestCase
from django.urls import reverse

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
