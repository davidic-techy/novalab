from rest_framework import viewsets, decorators, response, status, permissions
from django.utils import timezone
from .models import ProjectTemplate, Project
from .serializers import ProjectTemplateSerializer, ProjectSerializer
from .generator import ProjectGenerator
from .grader import ProjectAutoGrader

class ProjectTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Library of available project templates.
    """
    queryset = ProjectTemplate.objects.all()
    serializer_class = ProjectTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.action(detail=True, methods=['post'])
    def initialize(self, request, pk=None):
        """
        POST /api/projects/templates/{id}/initialize/
        Creates a new project instance for the student with scaffolded files.
        """
        template = self.get_object()
        user = request.user

        # Check if already exists
        if Project.objects.filter(user=user, template=template).exists():
            return response.Response(
                {"error": "You already have an active project for this template."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generate Files
        initial_files = ProjectGenerator.generate_scaffold(template, user)

        # Create Project
        project = Project.objects.create(
            user=user,
            template=template,
            artifact_data=initial_files,
            status=Project.Status.DRAFT
        )

        return response.Response(ProjectSerializer(project).data)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Manage active projects.
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    @decorators.action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """
        POST /api/projects/my-projects/{id}/submit/
        Runs the auto-grader and finalizes the project.
        """
        project = self.get_object()
        
        if project.status == Project.Status.GRADED:
             return response.Response({"error": "Already graded."}, status=400)

        # 1. Update with latest code from request (optional)
        if 'artifact_data' in request.data:
            project.artifact_data = request.data['artifact_data']

        # 2. Run Auto-Grader
        score, feedback = ProjectAutoGrader.grade(project)

        # 3. Save
        project.grade_score = score
        project.feedback = feedback
        project.status = Project.Status.GRADED # Or SUBMITTED if teacher review needed
        project.submitted_at = timezone.now()
        project.save()

        return response.Response(ProjectSerializer(project).data)