from django.urls import path
from .views import GoogleLoginView, UserProfileView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # The Google Login Endpoint
    path('google/', GoogleLoginView.as_view(), name='google_login'),
    
    # "Who am I?" Endpoint
    path('me/', UserProfileView.as_view(), name='user_profile'),

    # Standard JWT Refresh (If access token expires, use refresh token to get a new one)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]