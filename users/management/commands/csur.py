from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='Admin@adminow.ru',
            first_name='Admin',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('Ad.Min00')
        user.save()
