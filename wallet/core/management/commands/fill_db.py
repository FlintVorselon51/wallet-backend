from django.core.management import BaseCommand, call_command
from django.contrib.auth import get_user_model

User = get_user_model()


fixtures = ('currencies.json', 'wallets.json', 'transaction_categories.json', 'transactions.json')


class Command(BaseCommand):
    help = 'Flush the database, create a superuser and fill the database with initial data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput', action='store_true', help='Tells Django to NOT prompt the user for input of any kind.'
        )

    def handle(self, *args, **options):
        noinput = options['noinput']
        if noinput:
            call_command('flush', '--noinput')
            User.objects.create_superuser(email='admin@gmail.com', password='1234')
        else:
            call_command('flush')
            call_command('createsuperuser')
        call_command('loaddata', *fixtures)
