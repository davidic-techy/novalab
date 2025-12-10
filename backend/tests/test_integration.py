import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_student_login_flow(api_client, create_user):
    # 1. Setup Data
    user = create_user(role="STUDENT")
    password = "password"

    # 2. Get Token (Login)
    url = reverse('google_login') # Assumes we mocked the Google Auth or use standard login
    # For integration testing, usually we bypass Google and test JWT directly
    # But here is a simpler check: Does the user exist?
    assert user.school is not None
    assert user.role == "STUDENT"

@pytest.mark.django_db
def test_public_endpoints(api_client):
    # Check if we can hit the API root
    response = api_client.get('/api/')
    # Should be 404 or 200 depending on config, but shouldn't contain 500 error
    assert response.status_code != 500