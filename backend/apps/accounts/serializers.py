from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 
            'role', 'avatar', 'bio', 'is_email_verified'
        ]
        read_only_fields = ['role', 'is_email_verified', 'email'] # Prevent users from hacking their role via API