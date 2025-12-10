from rest_framework import serializers
from .models import ProjectTemplate, Project

class ProjectTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTemplate
        fields = ['id', 'title', 'description', 'difficulty', 'created_at']

class ProjectSerializer(serializers.ModelSerializer):
    template_title = serializers.CharField(source='template.title', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'template', 'template_title', 'status', 
            'artifact_data', 'grade_score', 'feedback', 'submitted_at'
        ]
        read_only_fields = ['status', 'grade_score', 'feedback', 'submitted_at']