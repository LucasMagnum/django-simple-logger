import logging
import json


class DBLogRecordHandler(logging.Handler):
    def emit(self, record):
        from .models import LogRecord, ExceptionRecord

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
