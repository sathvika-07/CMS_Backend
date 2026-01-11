from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Lesson, Program


class Command(BaseCommand):
    help = 'Publish scheduled lessons whose publish_at time has passed'

    def handle(self, *args, **options):
        now = timezone.now()
        
        # Query all lessons that are scheduled and ready to be published
        scheduled_lessons = Lesson.objects.filter(
            status='scheduled',
            publish_at__lte=now
        )
        
        published_count = 0
        
        for lesson in scheduled_lessons:
            # Update lesson status
            lesson.status = 'published'
            lesson.published_at = timezone.now()
            lesson.save()
            
            published_count += 1
            
            # Check and update program status if needed
            program = lesson.term.program
            if program.status != 'published':
                program.status = 'published'
                program.published_at = timezone.now()
                program.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Auto-published program: {program.title}'
                    )
                )
        
        # Print summary
        if published_count > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully published {published_count} lesson(s)'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING('No lessons to publish at this time')
            )
