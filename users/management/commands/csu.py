from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Команда для входа пользователя."""
    def handle(self, *args, **options):
        user = User.objects.create(email='admin@example.com')
        user.set_password('admin')
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()