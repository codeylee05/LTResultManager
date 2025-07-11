from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = 'Create a superuser if one does not exist.'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'Admin')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@mail.com')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'Admin0000')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(
                f"Superuser '{username}' created."))
        else:
            self.stdout.write(self.style.WARNING(
                f"Superuser '{username}' already exists."))
