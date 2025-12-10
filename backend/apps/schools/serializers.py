from rest_framework import serializers
from .models import School, Classroom

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'slug', 'domain', 'logo', 'is_active']
        read_only_fields = ['id', 'slug', 'is_active'] # Only Admins should change these

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'name', 'grade_level', 'school']