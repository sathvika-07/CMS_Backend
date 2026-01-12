"""ViewSets for CMS CRUD with staff-only writes and list filtering/search."""

from rest_framework import viewsets
from .models import Program, Topic, Term, Lesson
from .serializers import ProgramSerializer, TopicSerializer, TermSerializer, LessonSerializer
from .permissions import StaffWritePermission

class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [StaffWritePermission]
    filterset_fields = ['status', 'language_primary', 'topics__name']
    search_fields = ['title', 'description', 'topics__name']
    ordering_fields = ['created_at', 'updated_at', 'published_at', 'title']
    ordering = ['-created_at']

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [StaffWritePermission]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

class TermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer
    permission_classes = [StaffWritePermission]
    filterset_fields = ['program', 'term_number']
    search_fields = ['title', 'program__title']
    ordering_fields = ['term_number', 'created_at']
    ordering = ['term_number']

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [StaffWritePermission]
    filterset_fields = ['term', 'status', 'content_type', 'content_language_primary']
    search_fields = ['title', 'term__program__title']
    ordering_fields = ['lesson_number', 'publish_at', 'published_at', 'created_at']
    ordering = ['lesson_number']
