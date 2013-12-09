import datetime
import logging

from optparse import make_option

from django.core.management.base import BaseCommand

from simplelogger.models import LogRecord


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = '''
        Can be run as a cronjob or directly to clean out old exceptions from
        the database.

        By default will delete all exceptions older than 3 days.

        But you can choose number of days
        >>> python manage.py simplelogger_cleanexceptions --days=7
    '''

    option_list = BaseCommand.option_list + (
        make_option(
            '--days',
            dest='days',
            default=3,
            type="int",
            help='Define number of days for delete a exception'
        ),
    )

    def handle(self, *args, **options):
        today = datetime.date.today()
        expire_date = today - datetime.timedelta(days=options['days'])

        self.stdout.write(
            'Delete exceptions created before %s \n' % expire_date
        )

        logs = LogRecord.objects.filter(added_on__lt=expire_date)
        count = logs.count()
        logs.delete()

        self.stdout.write('%s exceptions was deleted \n' % count)

        logger_msg = (
            'Clean exceptions command was executed %s. \n'
            '%s exceptions older than %s was deleted \n.' % (
                datetime.datetime.now(),
                count,
                expire_date)
        )
        logger.debug(logger_msg)
