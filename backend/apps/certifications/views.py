from rest_framework import viewsets, permissions, decorators
from django.http import HttpResponse
from .models import Certificate, UserBadge
from .serializers import CertificateSerializer, UserBadgeSerializer
from .generator import CertificateGenerator

class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View and Download Certificates.
    """
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Certificate.objects.filter(user=self.request.user)

    @decorators.action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        GET /api/certifications/certificates/{id}/download/
        Generates the PDF on the fly and returns it.
        """
        certificate = self.get_object()
        
        # Generate PDF
        pdf_buffer = CertificateGenerator.generate(certificate)
        
        # Return as File Response
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        filename = f"NovaLab_Certificate_{certificate.id}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response

class MyBadgesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List badges earned by the student.
    """
    serializer_class = UserBadgeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserBadge.objects.filter(user=self.request.user)