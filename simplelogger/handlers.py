import logging
import json

from django.conf import settings


class DBLogRecordHandler(logging.Handler):
    def emit(self, record):
        from .models import LogRecord, ExceptionRecord

        # if DEBUG is active, ignore django.db.backends logs
        # when DEBUG is active  django.db.backends sends a log message
        # to each hit on Database.
        # if you don't ignore them, loop forever.
        if settings.DEBUG:
            if 'django.db.backends' == record.name:
                return

        if record.exc_info:
            ExceptionRecord.create_from_exception(
                sender=None, request=None, exc_info=record.exc_info)

        extra = {
            'module': record.module,
            'pathname': record.pathname,
            'name': record.name,
            'args': record.args,
        }

        LogRecord.add(
            name=record.name.split('.')[0],
            msg=record.msg,
            level=record.levelno,
            extra=json.dumps(extra),
        )
