from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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
from main.serializers import (
    BioItemSerializer,
    CandidateProjectSerializer,
    CandidateSerializer,
    CandidateSkillSerializer,
    CandidateSummarySerializer,
    ContactSerializer,
    ContactTypeSerializer,
    ProjectSerializer,
    SkillSerializer,
    UserRegistrationSerializer,
)


class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]


class CandidateSummaryViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSummarySerializer
    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]


class BioItemViewSet(viewsets.ModelViewSet):
    queryset = BioItem.objects.all()
    serializer_class = BioItemSerializer
    permission_classes = [IsAuthenticated]


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]


class CandidateSkillViewSet(viewsets.ModelViewSet):
    queryset = CandidateSkill.objects.all()
    serializer_class = CandidateSkillSerializer
    http_method_names = ["get", "post", "delete"]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        candidate_skill = self.get_object()
        skill = candidate_skill.skill

        candidate_skill.delete()

        if not CandidateSkill.objects.filter(skill=skill).exists():
            skill.delete()

        return Response(
            {"detail": "CandidateSkill and orphaned Skill (if any) deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]


class CandidateProjectViewSet(viewsets.ModelViewSet):
    queryset = CandidateProject.objects.all()
    serializer_class = CandidateProjectSerializer
    http_method_names = ["get", "post", "delete"]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        candidate_project = self.get_object()
        project = candidate_project.project

        candidate_project.delete()

        if not CandidateProject.objects.filter(project=project).exists():
            project.delete()

        return Response(
            {"detail": "CandidateProject and orphaned Project (if any) deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]


class ContactTypeViewSet(viewsets.ModelViewSet):
    queryset = ContactType.objects.all()
    serializer_class = ContactTypeSerializer
    permission_classes = [IsAuthenticated]
