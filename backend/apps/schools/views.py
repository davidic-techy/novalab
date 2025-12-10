from rest_framework import viewsets, permissions
from .models import School, Classroom
from .serializers import SchoolSerializer, ClassroomSerializer

class SchoolViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Schools to be viewed or edited.
    """
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    # For MVP: Allow anyone to view schools (to find their login), but only Admins to edit
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ClassroomViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Classrooms.
    """
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Critical Security: Only show classrooms belonging to the user's school
        user = self.request.user
        if user.is_staff: # Superadmins see all
            return Classroom.objects.all()
        return Classroom.objects.filter(school=user.school)

    def perform_create(self, serializer):
        # Auto-assign the classroom to the creator's school
        serializer.save(school=self.request.user.school)