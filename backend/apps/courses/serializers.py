from rest_framework import serializers
from .models import Course, Module, Lesson, Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'options', 'order']
        # Note: We intentionally exclude 'correct_answer' so students can't inspect the API to cheat.

class LessonSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'type', 'content', 'duration_minutes', 'order', 'questions']

class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'order', 'lessons']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'description', 'thumbnail', 'instructor', 'created_at']

class CourseDetailSerializer(CourseSerializer):
    """
    Includes the full curriculum tree. Used for the Course Detail page.
    """
    modules = ModuleSerializer(many=True, read_only=True)
    
    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['modules']