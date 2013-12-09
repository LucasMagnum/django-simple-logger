import logging

from optparse import make_option

from django.core.management.base import BaseCommand
from django.core import management


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = '''
        Can be run as a cronjob or directly to clean out old exceptions from
        the database.

        By default will delete all exceptions and logs older than 3 days.

        But you can choose number of days
        >>> python manage.py simplelogger_cleanup --days=7
    '''

    option_list = BaseCommand.option_list + (
        make_option(
            '--days',
            dest='days',
            default=3,
            type="int",
            help='Define number of days for delete exceptions and logs'
        ),
    )

    def handle(self, *args, **options):
        management.call_command(
            'simplelogger_cleanlogs',
            days=options['days']
        )
        management.call_command(
            'simplelogger_cleanexceptions',
            days=options['days']
        )
