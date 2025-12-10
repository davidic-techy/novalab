from django.urls import path
from .views import EventIngestView, DashboardStatsView, SchoolStatsView, StudentStatsView

urlpatterns = [
    path('events/', EventIngestView.as_view(), name='ingest_event'),
    path('dashboard/', DashboardStatsView.as_view(), name='school_dashboard'),
    path('student-stats/', StudentStatsView.as_view()),
    path('school-stats/', SchoolStatsView.as_view()),
]