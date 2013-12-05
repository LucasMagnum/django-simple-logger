import logging

from django.test import TestCase

from simplelogger.models import LogRecord, ExceptionRecord

SIMPLE_LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {},
    'handlers': {
        'simplelogger_dbhandler': {
            'class': 'simplelogger.handlers.DBLogRecordHandler'
        }
    },
    'loggers': {
        'simplelogger_test': {
            'handlers': ['simplelogger_dbhandler'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}


class LoggingTestMixin(object):
    def setUp(self):
        # configure logging to use SIMPLE_LOGGING_CONFIG
        logging.config.dictConfig(SIMPLE_LOGGING_CONFIG)
        self.logger = logging.getLogger('simplelogger_test')


class LogModelTest(LoggingTestMixin, TestCase):
    def test_create_log_record_manually(self):
        """
            Test a shortcut `add` method of LogRecord to create a new LogRecord
        """
        LogRecord.add(
            name=self.logger,
            level=logging.DEBUG,
            msg='Testing a creation of new LogRecord',
        )
        self.assertEquals(LogRecord.count(), 1)

    def test_create_log_record_automatically(self):
        """
            Test logging configuration is working correctly,
            call a logger method and check if a record was added.
        """
        self.assertEquals(LogRecord.count(), 0)
        msg = 'Testing a create a new LogRecord automatically'

        self.logger.debug(msg)
        self.assertEquals(LogRecord.count(), 1)

        log = LogRecord.objects.get()

        self.assertEquals(msg, log.msg)
        self.assertEquals(logging.DEBUG, log.level)


class ExceptionModelTest(LoggingTestMixin, TestCase):
    def test_create_exception_record_manually(self):
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
            ExceptionRecord.create_from_exception(sender=None)

        self.assertEquals(ExceptionRecord.count(), 1)

    def test_create_exception_record_automatically(self):
        self.assertEquals(ExceptionRecord.count(), 0)

        try:
            1/0
        except ZeroDivisionError:
            self.logger.exception('Test create a exception automatically')

        self.assertEquals(ExceptionRecord.count(), 1)

        exception = ExceptionRecord.objects.get()

        self.assertEquals(exception.type, 'ZeroDivisionError')

