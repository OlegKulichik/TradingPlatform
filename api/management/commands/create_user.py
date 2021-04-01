from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.state import User


class Command(BaseCommand):
    help = 'Сreating a different number of users'

    def add_arguments(self, parser):
        parser.add_argument(
            'total',
            type=int,
            help='Indicates the number of users to be created')

        parser.add_argument(
            '-p',
            '--prefix',
            type=str,
            help='Define a username prefix', )

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        prefix = kwargs['prefix']

        for i in range(total):
            if prefix:
                username = '{prefix}_{random_string}'.format(prefix=prefix, random_string=get_random_string())
            else:
                username = get_random_string()
            User.objects.create_user(username=username, email='', password='123')
