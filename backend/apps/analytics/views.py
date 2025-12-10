from rest_framework import viewsets, views, response, status, permissions
from django.db import models # Generic Django models
from django.db.models import Avg, Count, Sum

# Import YOUR models
from .models import DailyStats, Event
from .serializers import EventSerializer, DailyStatsSerializer
from .collectors import EventCollector
from .processors import AnalyticsProcessor

# Import models from OTHER apps
from apps.courses.models import Course
from apps.certifications.models import Certificate, UserBadge
from apps.projects.models import Project
from apps.courses.serializers import CourseSerializer

# ... Rest of the file ...
class EventIngestView(views.APIView):
    """
    POST /api/analytics/events/
    Frontend sends telemetry here (e.g., "Student clicked Start Lab").
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            EventCollector.capture(
                user=request.user,
                event_type=serializer.validated_data['event_type'],
                metadata=serializer.validated_data.get('metadata')
            )
            return response.Response({"status": "captured"}, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DashboardStatsView(views.APIView):
    """
    GET /api/analytics/dashboard/
    Returns aggregated stats for the user's school.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # 1. Trigger a fresh aggregation (Real-time update)
        # In production, cache this or rely on a background job
        if request.user.school:
            AnalyticsProcessor.aggregate_school_stats(request.user.school.id)

            # 2. Fetch Data (Last 7 days)
            stats = DailyStats.objects.filter(school=request.user.school).order_by('-date')[:7]
            return response.Response(DailyStatsSerializer(stats, many=True).data)

        return response.Response([])


class StudentStatsView(views.APIView):
    """
    GET /api/analytics/student-stats/
    Returns personal progress AND recommended courses.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # 1. Existing Stats Logic
        badges_earned = UserBadge.objects.filter(user=user).count()
        total_xp = UserBadge.objects.filter(user=user).aggregate(Sum('badge__xp_value'))['badge__xp_value__sum'] or 0
        avg_grade = Project.objects.filter(user=user, status='GRADED').aggregate(Avg('grade_score'))['grade_score__avg'] or 0
        projects_completed = Project.objects.filter(user=user, status='GRADED').count()

        # 2. NEW: Recommendation Logic
        # Get IDs of courses the student has already finished (has a certificate)
        completed_course_ids = Certificate.objects.filter(user=user).values_list('course_id', flat=True)

        # Find courses that are:
        # A. Published
        # B. Available to this user's school OR Global (school is null)
        # C. NOT in the completed list
        recommended = Course.objects.filter(
            is_published=True
        ).filter(
            models.Q(school=user.school) | models.Q(school__isnull=True)
        ).exclude(
            id__in=completed_course_ids
        ).order_by('-created_at')[:3] # Show the latest 3

        return response.Response({
            "xp": total_xp,
            "badges": badges_earned,
            "avg_grade": round(avg_grade, 1),
            "projects_completed": projects_completed,
            "recommendations": CourseSerializer(recommended, many=True).data # <--- SENDING THIS NOW
        })
    """
    GET /api/analytics/student-stats/
    Returns personal progress for the logged-in student.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # 1. Calculate XP / Badges
        badges_earned = UserBadge.objects.filter(user=user).count()
        total_xp = UserBadge.objects.filter(user=user).aggregate(Sum('badge__xp_value'))['badge__xp_value__sum'] or 0

        # 2. Project Grades
        avg_grade = Project.objects.filter(user=user, status='GRADED').aggregate(Avg('grade_score'))['grade_score__avg'] or 0

        # 3. Learning Velocity (Events in last 7 days)
        # (Simplified for MVP: Just returning raw counts)
        projects_completed = Project.objects.filter(user=user, status='GRADED').count()

        return response.Response({
            "xp": total_xp,
            "badges": badges_earned,
            "avg_grade": round(avg_grade, 1),
            "projects_completed": projects_completed
        })

class SchoolStatsView(views.APIView):
    """
    GET /api/analytics/school-stats/
    Returns aggregate data for the School Admin/Teacher.
    """
    permission_classes = [permissions.IsAuthenticated] # Add IsSchoolAdmin permission in real app

    def get(self, request):
        school = getattr(request.user, 'school', None)
        if not school:
            return response.Response({"error": "No school assigned"}, status=400)

        # 1. Total Students
        # Note: We assume 'STUDENT' is the role key defined in User model
        total_students = school.users.filter(role='STUDENT').count()
        
        # 2. Active Projects
        active_projects = Project.objects.filter(user__school=school, status='DRAFT').count()
        
        # 3. Leaderboard (Top 5 Students by Badges)
        leaderboard = UserBadge.objects.filter(user__school=school) \
            .values('user__first_name', 'user__last_name', 'user__email') \
            .annotate(badge_count=Count('badge')) \
            .order_by('-badge_count')[:5]

        return response.Response({
            "total_students": total_students,
            "active_projects": active_projects,
            "leaderboard": leaderboard
        })