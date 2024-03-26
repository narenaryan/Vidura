from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Create a superuser from environment variables'

    def handle(self, *args, **options):
        # 判断Super用户是否存在
        user = User.objects.filter(is_superuser=True)
        if user:
            print('Superuser already exists')
            return

        username = os.environ.get('SUPERUSER_NAME')
        email = os.environ.get('SUPERUSER_EMAIL')
        password = os.environ.get('SUPERUSER_PASSWORD')

        if not User.objects.filter(username=username).exists():
            print(f"Creating superuser: {username}")
            User.objects.create_superuser(username=username, email=email, password=password)
            print("Superuser created successfully.")
        else:
            print("Superuser creation skipped: user already exists.")
