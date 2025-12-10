from rest_framework import viewsets, decorators, response, status, permissions
from django.shortcuts import get_object_or_404
from .models import Course, Lesson
from .serializers import CourseSerializer, CourseDetailSerializer, LessonSerializer
from .quiz_engine import QuizEngine

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Lists available courses.
    """
    queryset = Course.objects.filter(is_published=True)
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Fetches lesson details.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.action(detail=True, methods=['post'])
    def submit_quiz(self, request, pk=None):
        """
        Custom endpoint to grade a quiz.
        Payload: { "answers": { "101": "a", "102": "c" } }
        """
        lesson = self.get_object()
        
        if lesson.type != Lesson.ContentType.QUIZ:
            return response.Response(
                {"error": "This lesson is not a quiz."}, status=status.HTTP_400_BAD_REQUEST
            )

        student_answers = request.data.get('answers', {})
        score, details = QuizEngine.grade_submission(lesson, student_answers)

        # TODO: Save this score to a 'StudentProgress' model (in Analytics app)
        
        return response.Response({
            "score": score,
            "passed": score >= 70,
            "results": details
        })