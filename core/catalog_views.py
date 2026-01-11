from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Exists, OuterRef
from .models import Program, Lesson
from .serializers import CatalogProgramSerializer, CatalogLessonSerializer


@api_view(['GET'])
def list_catalog_programs(request):
    """
    List all programs that have at least one published lesson.
    Supports filters: language (language_primary), topic (topic name)
    Supports pagination: limit (default 10), offset (default 0)
    """
    # Get query parameters
    language = request.GET.get('language')
    topic_filter = request.GET.get('topic')
    limit = int(request.GET.get('limit', 10))
    offset = int(request.GET.get('offset', 0))
    
    # Subquery to check if program has published lessons
    published_lessons_exist = Lesson.objects.filter(
        term__program=OuterRef('pk'),
        status='published'
    )
    
    # Base query: only programs with published lessons
    queryset = Program.objects.filter(
        Exists(published_lessons_exist)
    ).distinct()
    
    # Apply language filter
    if language:
        queryset = queryset.filter(language_primary=language)
    
    # Apply topic filter
    if topic_filter:
        queryset = queryset.filter(
            topics__name__icontains=topic_filter
        ).distinct()
    
    # Get total count before pagination
    total_count = queryset.count()
    
    # Apply pagination
    programs = queryset[offset:offset + limit]
    
    # Serialize
    serializer = CatalogProgramSerializer(programs, many=True)
    
    # Prepare response with pagination metadata
    response_data = {
        'count': total_count,
        'limit': limit,
        'offset': offset,
        'results': serializer.data
    }
    
    # Create response with cache headers
    response = Response(response_data)
    response['Cache-Control'] = 'public, max-age=300'  # Cache for 5 minutes
    
    return response


@api_view(['GET'])
def get_catalog_program(request, id):
    """
    Get a single program by ID.
    Only returns if the program has at least one published lesson.
    """
    try:
        # Check if program has published lessons
        published_lessons_exist = Lesson.objects.filter(
            term__program_id=id,
            status='published'
        ).exists()
        
        if not published_lessons_exist:
            return Response(
                {'error': 'Program not found or has no published content'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        program = Program.objects.get(id=id)
        serializer = CatalogProgramSerializer(program)
        
        # Create response with cache headers
        response = Response(serializer.data)
        response['Cache-Control'] = 'public, max-age=300'  # Cache for 5 minutes
        
        return response
        
    except Program.DoesNotExist:
        return Response(
            {'error': 'Program not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def get_catalog_lesson(request, id):
    """
    Get a single lesson by ID.
    Only returns published lessons.
    """
    try:
        lesson = Lesson.objects.get(id=id, status='published')
        serializer = CatalogLessonSerializer(lesson)
        
        # Create response with cache headers
        response = Response(serializer.data)
        response['Cache-Control'] = 'public, max-age=300'  # Cache for 5 minutes
        
        return response
        
    except Lesson.DoesNotExist:
        return Response(
            {'error': 'Lesson not found or not published'},
            status=status.HTTP_404_NOT_FOUND
        )
