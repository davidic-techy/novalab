import pytest
from rest_framework.test import APIClient
from apps.accounts.models import User
from apps.schools.models import School

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_school():
    def _create_school(name="Test School", slug="test-school"):
        return School.objects.create(name=name, slug=slug)
    return _create_school

@pytest.fixture
def create_user(create_school):
    def _create_user(email="test@novalab.io", password="password", role="STUDENT"):
        school = create_school()
        # FIX: Explicitly pass username=email to satisfy Django
        user = User.objects.create_user(
            username=email, 
            email=email, 
            password=password, 
            role=role, 
            school=school
        )
        return user
    return _create_user