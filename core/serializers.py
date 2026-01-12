"""DRF serializers with validation for language and scheduling rules."""

from django.utils import timezone
from rest_framework import serializers
from .models import Program, Term, Lesson, Topic
from .services import ensure_primary_in_available


class ProgramSerializer(serializers.ModelSerializer):
    languages_available = serializers.ListField(
        child=serializers.CharField(max_length=5),
        allow_empty=False,
    )

    class Meta:
        model = Program
        fields = [
            'id',
            'title',
            'description',
            'language_primary',
            'languages_available',
            'status',
            'published_at',
            'created_at',
            'updated_at',
        ]

    def validate_languages_available(self, value):
        if not all(value):
            raise serializers.ValidationError('languages_available cannot contain empty values.')
        return value

    def validate(self, attrs):
        language_primary = attrs.get(
            'language_primary',
            getattr(self.instance, 'language_primary', None),
        )
        languages_available = attrs.get(
            'languages_available',
            getattr(self.instance, 'languages_available', []),
        )

        ensure_primary_in_available(language_primary, languages_available, 'languages_available')

        status = attrs.get('status', getattr(self.instance, 'status', None))
        published_at = attrs.get('published_at', getattr(self.instance, 'published_at', None))
        now = timezone.now()

        if status == 'published':
            if not published_at:
                raise serializers.ValidationError({
                    'published_at': 'published_at is required when status is published.',
                })
            if published_at > now:
                raise serializers.ValidationError({
                    'published_at': 'published_at cannot be in the future when status is published.',
                })

        return attrs


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class TermSerializer(serializers.ModelSerializer):
    program = ProgramSerializer(read_only=True)
    program_id = serializers.PrimaryKeyRelatedField(
        queryset=Program.objects.all(),
        source='program',
        write_only=True,
    )
    term_number = serializers.IntegerField(min_value=1)

    class Meta:
        model = Term
        fields = [
            'id',
            'program',
            'program_id',
            'term_number',
            'title',
            'created_at',
        ]


class LessonSerializer(serializers.ModelSerializer):
    term = TermSerializer(read_only=True)
    term_id = serializers.PrimaryKeyRelatedField(
        queryset=Term.objects.all(),
        source='term',
        write_only=True,
    )
    lesson_number = serializers.IntegerField(min_value=1)
    duration_ms = serializers.IntegerField(min_value=0, required=False, allow_null=True)
    content_languages_available = serializers.ListField(
        child=serializers.CharField(max_length=5),
        allow_empty=False,
    )
    content_urls_by_language = serializers.DictField(
        child=serializers.CharField(allow_blank=False),
        allow_empty=False,
    )

    class Meta:
        model = Lesson
        fields = [
            'id',
            'term',
            'term_id',
            'lesson_number',
            'title',
            'content_type',
            'duration_ms',
            'is_paid',
            'content_language_primary',
            'content_languages_available',
            'content_urls_by_language',
            'status',
            'publish_at',
            'published_at',
            'created_at',
            'updated_at',
        ]

    def validate_content_languages_available(self, value):
        if not all(value):
            raise serializers.ValidationError('content_languages_available cannot contain empty values.')
        return value

    def validate_content_urls_by_language(self, value):
        for lang, url in value.items():
            if not lang:
                raise serializers.ValidationError('Language keys cannot be empty in content_urls_by_language.')
            if not url:
                raise serializers.ValidationError('Content URLs cannot be empty.')
        return value

    def validate(self, attrs):
        status = attrs.get('status', getattr(self.instance, 'status', 'draft'))
        publish_at = attrs.get('publish_at', getattr(self.instance, 'publish_at', None))
        published_at = attrs.get('published_at', getattr(self.instance, 'published_at', None))
        content_languages_available = attrs.get(
            'content_languages_available',
            getattr(self.instance, 'content_languages_available', []),
        )
        content_language_primary = attrs.get(
            'content_language_primary',
            getattr(self.instance, 'content_language_primary', None),
        )
        urls = attrs.get(
            'content_urls_by_language',
            getattr(self.instance, 'content_urls_by_language', {}),
        )

        now = timezone.now()
        errors = {}

        try:
            ensure_primary_in_available(
                content_language_primary,
                content_languages_available,
                'content_languages_available',
            )
        except serializers.ValidationError as exc:
            errors.update(exc.detail)

        if urls:
            if content_language_primary and not urls.get(content_language_primary):
                errors['content_urls_by_language'] = 'Provide a content URL for the primary language.'

            invalid_keys = [lang for lang in urls.keys() if lang not in content_languages_available]
            if invalid_keys:
                errors['content_urls_by_language'] = (
                    'Content URLs include languages not declared in content_languages_available: '
                    + ', '.join(sorted(invalid_keys))
                )

        if status == 'scheduled':
            if not publish_at:
                errors['publish_at'] = 'publish_at is required when status is scheduled.'
            elif publish_at <= now:
                errors['publish_at'] = 'publish_at must be in the future for scheduled lessons.'

        if status == 'published':
            if not published_at:
                errors['published_at'] = 'published_at is required when status is published.'
            elif published_at > now:
                errors['published_at'] = 'published_at cannot be in the future.'

            if publish_at and publish_at > published_at:
                errors['publish_at'] = 'publish_at must be on or before published_at.'

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


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

