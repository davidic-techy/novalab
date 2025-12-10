from rest_framework import views, response, status, permissions
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from .oauth import validate_google_token  # The helper we wrote earlier

User = get_user_model()

class GoogleLoginView(views.APIView):
    """
    Receives an ID Token from Google (frontend), verifies it, 
    and returns NovaLab JWT access/refresh tokens.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.data.get('token')
        if not token:
            return response.Response(
                {'error': 'No token provided'}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 1. Validate token with Google
            google_data = validate_google_token(token)
        except Exception as e:
            return response.Response(
                {'error': 'Invalid Google Token'}, status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Get or Create User
        email = google_data['email']
        first_name = google_data.get('given_name', '')
        last_name = google_data.get('family_name', '')
        
        # We try to get the user, or create them if they are new
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email, # Fallback username
                'first_name': first_name,
                'last_name': last_name,
                'is_email_verified': True
            }
        )

        # 3. Generate JWT Tokens (Access + Refresh)
        refresh = RefreshToken.for_user(user)

        return response.Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })

class UserProfileView(views.APIView):
    """
    Returns the currently logged-in user's details.
    Used by the Frontend to load the Dashboard.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return response.Response(serializer.data)