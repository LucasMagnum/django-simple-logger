import logging

from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings

from simplelogger.models import LogRecord, ExceptionRecord

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'simplelogger_dbhandler': {
            'class': 'simplelogger.handlers.DBLogRecordHandler'
        }
    },
    'loggers': {
        '': {
            'handlers': ['simplelogger_dbhandler'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}


@override_settings(LOGGING=settings.LOGGING)
class LogModelTest(TestCase):
    def test_create_log_record_manually(self):
        LogRecord.add(
            name=logging.getLogger(__name__),
            level=logging.DEBUG,
            msg='Testing a creation of new LogRecord',
        )
        self.assertEquals(LogRecord.count(), 1)


class ExceptionModelTest(TestCase):
    def test_create_exception_record(self):
        """
            Test to create a ExceptionRecord with
            `create_from_exception` method and check if `count` of all
            records are 1.

            Force a exception and call the `create_from_exception` method.
        """
        self.assertEquals(ExceptionRecord.count(), 0)

        try:
            1/0
        except:
            # pass sender keyword with None value
            ExceptionRecord.create_from_exception(sender=None)

        self.assertEquals(ExceptionRecord.count(), 1)
