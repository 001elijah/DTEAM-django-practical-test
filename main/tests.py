from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from CVProject.constants import API_URLS
from main.models import (
    BioItem,
    Candidate,
    CandidateProject,
    CandidateSkill,
    Contact,
    ContactType,
    Project,
    Skill,
)


class BaseTest(APITestCase):
    fixtures = ["users.json"]

    @classmethod
    def setUpTestData(cls):
        # Get user
        cls.user = User.objects.get(username="test_user")

    def setUp(self):
        # Login user
        self.client.login(username="test_user", password="test_password")


class CVViewTests(BaseTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Create a candidate
        cls.candidate = Candidate.objects.create(first_name="John", last_name="Doe")

        # Create and associate a bio
        cls.bio = BioItem.objects.create(
            bio_item="A seasoned software engineer.", candidate=cls.candidate
        )

        # Create a skill and associate with candidate
        cls.skill = Skill.objects.create(skill_name="Python")
        cls.candidate_skill = CandidateSkill.objects.create(
            candidate=cls.candidate, skill=cls.skill
        )

        # Create a project and associate with candidate
        cls.project = Project.objects.create(
            project_name="Test Project",
            project_description="A test project description.",
        )
        cls.candidate_project = CandidateProject.objects.create(
            candidate=cls.candidate, project=cls.project
        )

        # Create a contact type and contact
        cls.contact_type = ContactType.objects.create(contact_type="Email")
        cls.contact = Contact.objects.create(
            contact="john.doe@example.com",
            candidate=cls.candidate,
            contact_type=cls.contact_type,
        )

    def test_cv_list_view(self):
        # Test the CV list view
        url = reverse("cv_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Doe")

    def test_cv_detail_view(self):
        # Test the CV detail view
        url = reverse("cv_detail", args=[self.candidate.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Doe")
        self.assertContains(response, "A seasoned software engineer.")
        self.assertContains(response, "Python")
        self.assertContains(response, "Test Project")
        self.assertContains(response, "john.doe@example.com")


class CVCRUDTests(BaseTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Create initial data
        cls.skill = Skill.objects.create(skill_name="Python")
        cls.contact_type = ContactType.objects.create(contact_type="Email")

    def test_create_candidate(self):
        # Test creating a candidate
        candidate = Candidate.objects.create(first_name="Micah", last_name="Smith")
        self.assertEqual(candidate.first_name, "Micah")

    def test_read_candidate(self):
        # Test retrieving a created candidate
        candidate = Candidate.objects.create(first_name="Micah", last_name="Smith")
        retrieved_candidate = Candidate.objects.get(id=candidate.id)
        self.assertEqual(retrieved_candidate.first_name, "Micah")

    def test_update_candidate(self):
        # Test updating a candidate
        candidate = Candidate.objects.create(first_name="Micah", last_name="Smith")
        candidate.first_name = "Updated Micah"
        candidate.save()
        updated_candidate = Candidate.objects.get(id=candidate.id)
        self.assertEqual(updated_candidate.first_name, "Updated Micah")

    def test_delete_candidate(self):
        # Test deleting a candidate
        candidate = Candidate.objects.create(first_name="Micah", last_name="Smith")
        candidate_id = candidate.id
        candidate.delete()
        with self.assertRaises(Candidate.DoesNotExist):
            Candidate.objects.get(id=candidate_id)


class CandidateAPITests(BaseTest):
    fixtures = ["users.json", "candidates.json"]

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Create initial candidate for the test
        cls.candidate = Candidate.objects.get(first_name="John")

        # Define endpoints
        cls.list_url = API_URLS["candidates"]
        cls.detail_url = f"{cls.list_url}{cls.candidate.id}/"

    def test_list_candidates(self):
        # Test list endpoint for candidates
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["first_name"], "John")

    def test_retrieve_candidate(self):
        # Test retrieve endpoint for one candidate
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "John")
        self.assertEqual(response.data["last_name"], "Doe")

    def test_create_candidate(self):
        # Test create endpoint
        payload = {"first_name": "Micah", "last_name": "Smith"}
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["first_name"], "Micah")
        self.assertEqual(Candidate.objects.count(), 3)

    def test_update_candidate(self):
        # Test update endpoint
        payload = {"first_name": "Updated John", "last_name": "Doe"}
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Updated John")

    def test_delete_candidate(self):
        # Test delete endpoint
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Candidate.objects.count(), 1)


class BioItemAPITests(BaseTest):
    fixtures = ["users.json", "candidates.json", "bio_items.json"]

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Create a candidate
        cls.candidate = Candidate.objects.get(first_name="John")

        # Create a BioItem associated with the candidate
        cls.bio_item = BioItem.objects.get(pk=1)

        # Define endpoints
        cls.list_url = API_URLS["bio_items"]
        cls.detail_url = f"{cls.list_url}{cls.bio_item.id}/"

    def test_list_bio_items(self):
        # Test the list endpoint
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["bio_item"], "A seasoned software engineer.")

    def test_retrieve_bio_item(self):
        # Test retrieving a single bio item
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["bio_item"], "A seasoned software engineer.")
        self.assertEqual(response.data["candidate"], self.candidate.id)

    def test_duplicate_bio_creation_failure(self):
        # Attempt to create a new bio for the same candidate
        payload = {"bio_item": "Creative Thinker.", "candidate": self.candidate.id}
        response = self.client.post(self.list_url, payload)

        # Assert that the request fails due to the unique constraint
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "candidate", response.data
        )  # Ensure error refers to the candidate field
        self.assertEqual(
            BioItem.objects.count(), 2
        )  # Ensure only the initial bio exist

    def test_create_bio_item(self):
        # Create a new candidate and attach a new bio
        new_candidate = Candidate.objects.create(first_name="Micah", last_name="Smith")

        new_payload = {"bio_item": "Creative Thinker.", "candidate": new_candidate.id}
        response = self.client.post(self.list_url, new_payload)

        # Assert that this succeeds (status 201, created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["bio_item"], "Creative Thinker.")
        self.assertEqual(response.data["candidate"], new_candidate.id)
        self.assertEqual(BioItem.objects.count(), 3)  # Ensure three bios exist in total

    def test_update_bio_item(self):
        # Test updating an existing bio item
        payload = {
            "bio_item": "Updated Experienced Software Engineer.",
            "candidate": self.candidate.id,
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["bio_item"], "Updated Experienced Software Engineer."
        )

    def test_delete_bio_item(self):
        # Test deleting a bio item
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BioItem.objects.count(), 1)


class SkillAPITests(BaseTest):
    fixtures = ["users.json", "skills.json"]

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Create some initial skills
        cls.skill = Skill.objects.get(skill_name="Python")
        cls.another_skill = Skill.objects.get(skill_name="Django")

        # Define endpoints
        cls.list_url = API_URLS["skills"]
        cls.detail_url = f"{cls.list_url}{cls.skill.id}/"

    def test_list_skills(self):
        # Test listing all skills
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two skills exist in the database
        self.assertEqual(response.data[0]["skill_name"], "Python")

    def test_retrieve_skill(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["skill_name"], "Python")

    def test_create_skill(self):
        # Test creating a new skill
        payload = {"skill_name": "JavaScript"}
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["skill_name"], "JavaScript")
        self.assertEqual(Skill.objects.count(), 3)  # Ensure a new skill is created

    def test_update_skill(self):
        # Test updating an existing skill
        payload = {"skill_name": "Python Programming"}
        response = self.client.put(
            self.detail_url, payload, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["skill_name"], "Python Programming")
        self.skill.refresh_from_db()
        self.assertEqual(
            self.skill.skill_name, "Python Programming"
        )  # Ensure the DB is updated

    def test_delete_skill(self):
        # Test deleting a skill
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Skill.objects.count(), 1)  # Only one skill should remain


class CandidateSkillAPITests(BaseTest):
    fixtures = ["users.json", "candidates.json", "skills.json", "candidate_skills.json"]

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Create a candidate and skills
        cls.candidate = Candidate.objects.get(first_name="Jane")
        cls.skill = Skill.objects.get(skill_name="Python")
        cls.another_skill = Skill.objects.get(skill_name="Django")

        # Create a CandidateSkill relation
        cls.candidate_skill = CandidateSkill.objects.get(candidate=cls.candidate.id)

        # Define endpoints
        cls.list_url = API_URLS["candidate_skills"]
        cls.detail_url = f"{cls.list_url}{cls.candidate_skill.id}/"

    def test_list_candidate_skills(self):
        # Test listing all candidate skills
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["skill"], self.skill.id)
        self.assertEqual(response.data[1]["candidate"], self.candidate.id)

    def test_retrieve_candidate_skill(self):
        # Test retrieving a specific candidate skill
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["skill"], self.another_skill.id)
        self.assertEqual(response.data["candidate"], self.candidate.id)

    def test_create_candidate_skill(self):
        # Test creating a new candidate skill
        payload = {"candidate": self.candidate.id, "skill": self.another_skill.id}
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["skill"], self.another_skill.id)
        self.assertEqual(response.data["candidate"], self.candidate.id)
        self.assertEqual(
            CandidateSkill.objects.count(), 2
        )  # Confirm new candidate skill created

    def test_update_candidate_skill(self):
        # Expect 405 error for PUT requests
        payload = {"candidate": self.candidate.id, "skill": self.another_skill.id}
        response = self.client.put(
            self.detail_url, payload, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_candidate_skill(self):
        # Test deleting a candidate skill
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CandidateSkill.objects.count(), 1)  # Confirm it was deleted


class ProjectAPITests(BaseTest):
    fixtures = ["users.json", "projects.json"]

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Create some initial projects
        cls.project_first = Project.objects.get(pk=1)
        cls.project_second = Project.objects.get(pk=2)

        # Define endpoints
        cls.list_url = API_URLS["projects"]
        cls.detail_url = f"{cls.list_url}{cls.project_first.id}/"

    def test_list_projects(self):
        # Test listing all projects
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            response.data[0]["project_name"], self.project_first.project_name
        )
        self.assertEqual(
            response.data[1]["project_name"], self.project_second.project_name
        )

    def test_retrieve_project(self):
        # Test retrieving a specific project
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["project_name"], self.project_first.project_name)
        self.assertEqual(
            response.data["project_description"], self.project_first.project_description
        )

    def test_create_project(self):
        # Test creating a new project
        payload = {
            "project_name": "New Project",
            "project_description": "Description of New Project",
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["project_name"], "New Project")
        self.assertEqual(
            Project.objects.count(), 3
        )  # Ensure a new project is created in the database

    def test_update_project(self):
        # Test updating an existing project
        payload = {
            "project_name": "Updated Project One",
            "project_description": "Updated Description of Project One",
        }
        response = self.client.put(
            self.detail_url, payload, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["project_name"], "Updated Project One")
        self.project_first.refresh_from_db()
        self.assertEqual(self.project_first.project_name, "Updated Project One")
        self.assertEqual(
            self.project_first.project_description, "Updated Description of Project One"
        )

    def test_delete_project(self):
        # Test deleting a project
        detail_url = f"{self.list_url}{self.project_second.id}/"
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            Project.objects.count(), 1
        )  # Ensure the project is deleted from the database


class CandidateProjectAPITests(BaseTest):
    fixtures = [
        "users.json",
        "candidates.json",
        "projects.json",
        "candidate_projects.json",
    ]

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Create candidate and projects
        cls.candidate = Candidate.objects.get(first_name="John")
        cls.project_first = Project.objects.get(pk=1)
        cls.project_second = Project.objects.get(pk=2)

        # Associate a candidate with a project
        cls.candidate_project = CandidateProject.objects.get(candidate=cls.candidate.id)

        # Define endpoints
        cls.list_url = API_URLS["candidate_projects"]
        cls.detail_url = f"{cls.list_url}{cls.candidate_project.id}/"

    def test_list_candidate_projects(self):
        # Test listing all candidate projects
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["candidate"], self.candidate.id)

        project_response = response.data[0]["project"]
        self.assertEqual(project_response["id"], self.project_first.id)
        self.assertEqual(
            project_response["project_name"], self.project_first.project_name
        )
        self.assertEqual(
            project_response["project_description"],
            self.project_first.project_description,
        )

    def test_create_candidate_project(self):
        # Test creating a new candidate-project association
        payload = {
            "project": {
                "project_name": self.project_second.project_name,
                "project_description": self.project_second.project_description,
            },
            "candidate": self.candidate.id,
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["candidate"], self.candidate.id)

        project_response = response.data["project"]
        self.assertEqual(project_response["id"], self.project_second.id)
        self.assertEqual(
            project_response["project_name"], self.project_second.project_name
        )
        self.assertEqual(
            project_response["project_description"],
            self.project_second.project_description,
        )

        self.assertEqual(
            CandidateProject.objects.count(), 3
        )  # Ensure new association is created

    def test_delete_candidate_project(self):
        # Test deleting a candidate-project association
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            CandidateProject.objects.count(), 1
        )  # Ensure it is deleted from database

    def test_retrieve_candidate_project(self):
        # Test retrieving a specific candidate-project association
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["candidate"], self.candidate.id)

        project_response = response.data["project"]
        self.assertEqual(project_response["id"], self.project_first.id)
        self.assertEqual(
            project_response["project_name"], self.project_first.project_name
        )
        self.assertEqual(
            project_response["project_description"],
            self.project_first.project_description,
        )

    def test_update_candidate_project(self):
        # Test updating a candidate-project association with PUT (disallowed)
        payload = {"candidate": self.candidate.id, "project": self.project_second.id}
        response = self.client.put(
            self.detail_url, payload, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class ContactAPITests(BaseTest):
    fixtures = ["users.json", "candidates.json", "contact_types.json", "contacts.json"]

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Create a candidate
        cls.candidate = Candidate.objects.get(first_name="John")

        # Create a contact type
        cls.contact_type = ContactType.objects.get(pk=1)

        # Create an example contact
        cls.contact = Contact.objects.get(candidate=cls.candidate.id)

        # Define endpoints
        cls.list_url = API_URLS["contacts"]
        cls.detail_url = f"{cls.list_url}{cls.contact.id}/"

    def test_list_contacts(self):
        # Test listing all contacts
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # There are two contacts in the setup
        self.assertEqual(response.data[0]["id"], self.contact.id)
        self.assertEqual(response.data[0]["candidate"], self.candidate.id)
        self.assertEqual(response.data[0]["contact_type"], self.contact_type.id)
        self.assertEqual(response.data[0]["contact"], "john.doe@example.com")

    def test_retrieve_contact(self):
        # Test retrieving a single contact
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.contact.id)
        self.assertEqual(response.data["candidate"], self.candidate.id)
        self.assertEqual(response.data["contact_type"], self.contact_type.id)
        self.assertEqual(response.data["contact"], "john.doe@example.com")

    def test_create_contact(self):
        # Test creating a new contact
        payload = {
            "candidate": self.candidate.id,
            "contact_type": self.contact_type.id,
            "contact": "john.new@example.com",
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["candidate"], self.candidate.id)
        self.assertEqual(response.data["contact_type"], self.contact_type.id)
        self.assertEqual(response.data["contact"], "john.new@example.com")
        self.assertEqual(Contact.objects.count(), 3)  # Ensure a new contact is created

    def test_update_contact(self):
        # Test updating an existing contact
        payload = {
            "candidate": self.candidate.id,
            "contact_type": self.contact_type.id,
            "contact": "john.updated@example.com",
        }
        response = self.client.put(self.detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.contact, "john.updated@example.com")

    def test_delete_contact(self):
        # Test deleting a contact
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 1)  # Ensure the contact is deleted


class ContactTypeAPITests(BaseTest):
    fixtures = ["users.json", "contact_types.json"]

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Create some contact types
        cls.contact_type_first = ContactType.objects.get(pk=1)
        cls.contact_type_second = ContactType.objects.get(pk=2)

        # Define endpoints
        cls.list_url = API_URLS["contact_types"]
        cls.detail_url = f"{cls.list_url}{cls.contact_type_first.id}/"

    def test_list_contact_types(self):
        # Test listing all contact types
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # There are three ContactType instances
        self.assertEqual(response.data[0]["id"], self.contact_type_first.id)
        self.assertEqual(
            response.data[0]["contact_type"], self.contact_type_first.contact_type
        )
        self.assertEqual(response.data[1]["id"], self.contact_type_second.id)
        self.assertEqual(
            response.data[1]["contact_type"], self.contact_type_second.contact_type
        )

    def test_retrieve_contact_type(self):
        # Test retrieving a single contact type
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.contact_type_first.id)
        self.assertEqual(
            response.data["contact_type"], self.contact_type_first.contact_type
        )

    def test_create_contact_type(self):
        # Test creating a new contact type
        payload = {"contact_type": "Social Media"}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["contact_type"], "Social Media")
        self.assertEqual(
            ContactType.objects.count(), 4
        )  # Ensure a new contact type is created

    def test_update_contact_type(self):
        # Test updating an existing contact type
        payload = {"contact_type": "Updated Name"}
        response = self.client.put(self.detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact_type_first.refresh_from_db()
        self.assertEqual(self.contact_type_first.contact_type, "Updated Name")

    def test_delete_contact_type(self):
        # Test deleting a contact type
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            ContactType.objects.count(), 2
        )  # Only one contact type should remain


class CandidateSummaryAPITests(BaseTest):
    fixtures = [
        "users.json",
        "candidates.json",
        "bio_items.json",
        "skills.json",
        "candidate_skills.json",
        "projects.json",
        "candidate_projects.json",
        "contacts.json",
        "contact_types.json",
    ]

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Remove extra candidate
        Candidate.objects.get(first_name="John").delete()
        # Create a candidate
        cls.candidate = Candidate.objects.get(first_name="Jane")

        # Create a contact type and contact
        cls.contact_type = ContactType.objects.get(pk=1)
        cls.contact = Contact.objects.get(candidate=cls.candidate.id)

        # Create a bio item
        cls.bio = BioItem.objects.get(pk=2)

        # Create a skill
        cls.skill = Skill.objects.get(skill_name="Django")
        cls.candidate_skill = CandidateSkill.objects.get(candidate=cls.candidate.id)

        # Create a project
        cls.project = Project.objects.get(pk=2)
        cls.candidate_project = CandidateProject.objects.get(candidate=cls.candidate.id)

        # Define endpoints
        cls.list_url = API_URLS["candidate_summaries"]
        cls.detail_url = f"{cls.list_url}{cls.candidate.id}/"

    def test_list_candidate_summaries(self):
        # Test listing all candidate summaries
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 1
        )  # There is one candidate summary available
        self.assertEqual(response.data[0]["bio"]["bio_item"], self.bio.bio_item)
        self.assertEqual(
            response.data[0]["skills"][0]["skill_name"], self.skill.skill_name
        )
        self.assertEqual(
            response.data[0]["projects"][0]["project_name"], self.project.project_name
        )
        self.assertEqual(
            response.data[0]["contacts"][0]["contact"], self.contact.contact
        )

    def test_retrieve_candidate_summary(self):
        # Test retrieving a single candidate summary
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["bio"]["bio_item"], self.bio.bio_item)
        self.assertEqual(
            response.data["skills"][0]["skill_name"], self.skill.skill_name
        )
        self.assertEqual(
            response.data["projects"][0]["project_name"], self.project.project_name
        )
        self.assertEqual(response.data["contacts"][0]["contact"], self.contact.contact)

    def test_post_not_allowed(self):
        # Test that POST method is not allowed for candidate_summaries
        payload = {"some_field": "some_value"}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_not_allowed(self):
        # Test that PUT method is not allowed for candidate_summaries
        payload = {"some_field": "some_value"}
        response = self.client.put(self.detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_not_allowed(self):
        # Test that DELETE method is not allowed for candidate_summaries
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
