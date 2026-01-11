import uuid
from django.db import models

class Program(models.Model):
    STATUS_CHOICES = [('draft','draft'), ('published','published'), ('archived','archived')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    language_primary = models.CharField(max_length=5)
    languages_available = models.JSONField(default=list)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    programs = models.ManyToManyField(Program, related_name='topics')

class Term(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='terms')
    term_number = models.IntegerField()
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('program', 'term_number')
def _touch(): 
    pass

class Lesson(models.Model):
    TYPE_CHOICES = [('video','video'), ('article','article')]
    STATUS_CHOICES = [('draft','draft'), ('scheduled','scheduled'), ('published','published'), ('archived','archived')]

    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='lessons')
    lesson_number = models.IntegerField()
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    duration_ms = models.IntegerField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    content_language_primary = models.CharField(max_length=5)
    content_languages_available = models.JSONField(default=list)
    content_urls_by_language = models.JSONField(default=dict)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    publish_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('term', 'lesson_number')
