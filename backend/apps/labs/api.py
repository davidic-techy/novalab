from rest_framework import viewsets, decorators, response, status, permissions
from .models import Simulation, SandboxSession
from .serializers import SimulationSerializer, SandboxSessionSerializer
from .services import LabService

class SimulationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List of available labs (The Library).
    """
    queryset = Simulation.objects.all()
    serializer_class = SimulationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """
        POST /api/labs/simulations/{id}/start/
        Initializes a workspace for the user.
        """
        session = LabService.start_session(request.user, pk)
        return response.Response(SandboxSessionSerializer(session).data)

class WorkspaceViewSet(viewsets.ModelViewSet):
    """
    The active IDE endpoints.
    """
    serializer_class = SandboxSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SandboxSession.objects.filter(user=self.request.user)

    @decorators.action(detail=True, methods=['post'])
    def save_code(self, request, pk=None):
        """
        POST /api/labs/workspace/{id}/save_code/
        Auto-save functionality.
        """
        session = self.get_object()
        code = request.data.get('code')
        
        try:
            LabService.save_progress(session, code)
            return response.Response({"status": "saved", "timestamp": session.updated_at})
        except ValueError as e:
            return response.Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)