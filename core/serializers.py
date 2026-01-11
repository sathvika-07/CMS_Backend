from rest_framework import serializers
from .models import Program, Term, Lesson, Topic

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class TermSerializer(serializers.ModelSerializer):
    program = ProgramSerializer(read_only=True)

    class Meta:
        model = Term
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    term = TermSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'


# Catalog API Serializers (Public read-only)
class CatalogLessonSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'lesson_number', 'content_type', 'duration_ms', 
                  'is_paid', 'content_language_primary', 'content_languages_available',
                  'published_at', 'content_urls_by_language', 'status']


class CatalogProgramSerializer(serializers.ModelSerializer):
    terms = serializers.SerializerMethodField()
    topics = serializers.SerializerMethodField()
    
    class Meta:
        model = Program
        fields = ['id', 'title', 'description', 'language_primary', 
                  'languages_available', 'published_at', 'status', 'topics', 'terms']
    
    def get_topics(self, obj):
        return [{'id': str(topic.id), 'name': topic.name} for topic in obj.topics.all()]
    
    def get_terms(self, obj):
        # Only include terms with published lessons
        terms_data = []
        for term in obj.terms.all():
            published_lessons = term.lessons.filter(status='published')
            if published_lessons.exists():
                lessons_data = CatalogLessonSerializer(published_lessons, many=True).data
                terms_data.append({
                    'id': str(term.id),
                    'term_number': term.term_number,
                    'title': term.title,
                    'lessons': lessons_data
                })
        
        return terms_data

